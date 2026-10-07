<?php
/**
 * Single handler for every form on the site (quote modal, contact, service
 * request, technical support, job application). Each form POSTs a hidden
 * form_id; the destination inbox is looked up server-side from that id, never
 * trusted from client input, so a tampered field can't redirect mail elsewhere.
 */

require __DIR__ . '/smtp-mailer.php';
$SMTP_CONFIG = require __DIR__ . '/mail-config.php';

// TEST MODE: every form currently sends to this address instead of its real
// recipient below, for testing before go-live. Set to null to restore the
// normal per-form recipients in $FORMS.
$TEST_OVERRIDE_TO = null;

// form_id => [recipient, email subject, friendly label, return path (ar), return path (en)]
$FORMS = [
    'quote' => [
        'to' => 'wafi@jazdrm.com',
        'subject' => 'طلب عرض سعر جديد - jazdrm.com',
        'label' => 'طلب عرض سعر',
    ],
    'contact' => [
        'to' => 'wafi@jazdrm.com',
        'subject' => 'رسالة جديدة من نموذج اتصل بنا - jazdrm.com',
        'label' => 'اتصل بنا',
    ],
    'service-request' => [
        'to' => 'wafi@jazdrm.com',
        'subject' => 'طلب خدمة جديد - jazdrm.com',
        'label' => 'طلب خدمة',
    ],
    'technical-support' => [
        'to' => 'jazdrm@jazdrm.com',
        'subject' => 'تذكرة دعم فني جديدة - jazdrm.com',
        'label' => 'الدعم الفني',
    ],
    'job-application' => [
        'to' => 'wafi@jazdrm.com',
        'subject' => 'طلب توظيف جديد - jazdrm.com',
        'label' => 'التوظيف',
    ],
];

// Field label => friendly Arabic caption shown in the email body, in display order.
$FIELD_LABELS = [
    'name' => 'الاسم',
    'phone' => 'رقم الجوال',
    'email' => 'البريد الإلكتروني',
    'city' => 'المدينة / الفرع',
    'product' => 'المنتج أو الخدمة المطلوبة',
    'message' => 'الرسالة',
    'service_type' => 'نوع الخدمة المطلوبة',
    'preferred_date' => 'الموعد المفضل للزيارة',
    'job_details' => 'تفاصيل الطلب',
    'issue_type' => 'نوع المشكلة الفنية',
    'issue_description' => 'شرح تفصيلي للمشكلة',
    'position' => 'الوظيفة المستهدفة',
    'experience' => 'نبذة عن الخبرات والمهارات',
];

function reject($msg) {
    http_response_code(400);
    echo $msg;
    exit;
}

function single_line($s) {
    // Strip anything that could be used for email header injection.
    return trim(preg_replace('/[\r\n]+/', ' ', (string) $s));
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    reject('Invalid request method.');
}

$form_id = $_POST['form_id'] ?? '';
if (!isset($FORMS[$form_id])) {
    reject('Unknown form.');
}
$form = $FORMS[$form_id];
if ($TEST_OVERRIDE_TO) {
    $form['to'] = $TEST_OVERRIDE_TO;
}

$return_to = $_POST['return_to'] ?? '/';
// Only allow a same-site relative path back, never an absolute/external URL.
if (!preg_match('#^/[A-Za-z0-9/_\-]*$#', $return_to)) {
    $return_to = '/';
}

$lines = [];
$reply_to = null;
foreach ($FIELD_LABELS as $key => $label) {
    if (!isset($_POST[$key]) || $_POST[$key] === '') {
        continue;
    }
    $value = $key === 'message' || $key === 'job_details' || $key === 'issue_description' || $key === 'experience'
        ? trim(str_replace("\r\n", "\n", (string) $_POST[$key]))
        : single_line($_POST[$key]);
    if ($value === '') {
        continue;
    }
    $lines[] = "{$label}: {$value}";
    if ($key === 'email' && filter_var($value, FILTER_VALIDATE_EMAIL)) {
        $reply_to = $value;
    }
}

if (empty($lines)) {
    reject('Empty submission.');
}

$body = implode("\n", $lines) . "\n\n— " . $form['label'] . " · jazdrm.com\n";

$boundary = md5(uniqid((string) mt_rand(), true));
$headers = "";
if ($reply_to) {
    $headers .= "Reply-To: {$reply_to}\r\n";
}

$has_attachment = $form_id === 'job-application'
    && isset($_FILES['resume'])
    && $_FILES['resume']['error'] === UPLOAD_ERR_OK;

if ($has_attachment) {
    $file = $_FILES['resume'];
    $allowed_types = ['application/pdf'];
    $max_bytes = 5 * 1024 * 1024; // 5 MB

    if (!in_array($file['type'], $allowed_types, true) || $file['size'] > $max_bytes) {
        reject('Resume must be a PDF under 5MB.');
    }

    $file_content = chunk_split(base64_encode(file_get_contents($file['tmp_name'])));
    $filename = preg_replace('/[^A-Za-z0-9._\-]/', '_', basename($file['name']));

    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: multipart/mixed; boundary=\"{$boundary}\"\r\n";

    $message  = "--{$boundary}\r\n";
    $message .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $message .= "Content-Transfer-Encoding: 8bit\r\n\r\n";
    $message .= $body . "\r\n";
    $message .= "--{$boundary}\r\n";
    $message .= "Content-Type: application/pdf; name=\"{$filename}\"\r\n";
    $message .= "Content-Transfer-Encoding: base64\r\n";
    $message .= "Content-Disposition: attachment; filename=\"{$filename}\"\r\n\r\n";
    $message .= $file_content . "\r\n";
    $message .= "--{$boundary}--";
} else {
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $message = $body;
}

$result = smtp_send_mail($form['to'], $form['subject'], $headers, $message, $SMTP_CONFIG);
if (!$result['ok']) {
    error_log('send-form.php SMTP error (' . $form_id . '): ' . $result['error']);
}

header('Location: ' . $return_to . (strpos($return_to, '?') === false ? '?' : '&') . 'sent=' . ($result['ok'] ? '1' : '0') . '#' . $form_id . '-form');
exit;

<?php
/**
 * Single handler for every form on the site (quote modal, contact, service
 * request, technical support, job application). Each form POSTs a hidden
 * form_id; the destination inbox(es) are looked up server-side from that id,
 * never trusted from client input, so a tampered field can't redirect mail
 * elsewhere.
 */

require __DIR__ . '/smtp-mailer.php';
$SMTP_CONFIG = require __DIR__ . '/mail-config.php';

// TEST MODE: every form currently sends to this address instead of its real
// recipient(s) below, for testing before go-live. Set to null to restore the
// normal per-form recipients in $FORMS.
$TEST_OVERRIDE_TO = null;

// form_id => [recipient(s), email subject, friendly label]. 'to' may be a
// single address or an array of addresses (sent to each).
$FORMS = [
    'quote' => [
        'to' => ['sales-1@jazdrm.com', 'sales-2@jazdrm.com'],
        'subject' => 'طلب عرض سعر جديد - jazdrm.com',
        'label' => 'طلب عرض سعر',
    ],
    'contact' => [
        'to' => 'wafi@jazdrm.com',
        'subject' => 'رسالة جديدة من نموذج اتصل بنا - jazdrm.com',
        'label' => 'اتصل بنا',
    ],
    'service-request' => [
        'to' => 'jazdrm@jazdrm.com',
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

// Every form's file input accepts the same set of types: PDF, Word docs, images.
$ALLOWED_ATTACHMENT_TYPES = [
    'application/pdf' => 'pdf',
    'application/msword' => 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document' => 'docx',
    'image/jpeg' => 'jpg',
    'image/png' => 'png',
    'image/webp' => 'webp',
];
$MAX_ATTACHMENT_BYTES = 10 * 1024 * 1024; // 10 MB

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
$recipients = $TEST_OVERRIDE_TO ? [$TEST_OVERRIDE_TO] : (array) $form['to'];

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

// Every form's file field is named "attachment", except job-application's
// long-standing "resume" field - both are accepted, whichever is present.
$upload_field = isset($_FILES['resume']) ? 'resume' : (isset($_FILES['attachment']) ? 'attachment' : null);
$has_attachment = $upload_field !== null && $_FILES[$upload_field]['error'] === UPLOAD_ERR_OK;

if ($has_attachment) {
    $file = $_FILES[$upload_field];

    if (!isset($ALLOWED_ATTACHMENT_TYPES[$file['type']]) || $file['size'] > $MAX_ATTACHMENT_BYTES) {
        reject('Attachment must be a PDF, Word document, or image (JPG/PNG/WEBP) under 10MB.');
    }

    $file_content = chunk_split(base64_encode(file_get_contents($file['tmp_name'])));
    $filename = preg_replace('/[^A-Za-z0-9._\-]/', '_', basename($file['name']));
    $mime_type = $file['type'];

    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: multipart/mixed; boundary=\"{$boundary}\"\r\n";

    $message  = "--{$boundary}\r\n";
    $message .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $message .= "Content-Transfer-Encoding: 8bit\r\n\r\n";
    $message .= $body . "\r\n";
    $message .= "--{$boundary}\r\n";
    $message .= "Content-Type: {$mime_type}; name=\"{$filename}\"\r\n";
    $message .= "Content-Transfer-Encoding: base64\r\n";
    $message .= "Content-Disposition: attachment; filename=\"{$filename}\"\r\n\r\n";
    $message .= $file_content . "\r\n";
    $message .= "--{$boundary}--";
} else {
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $message = $body;
}

$all_ok = true;
foreach ($recipients as $to) {
    $result = smtp_send_mail($to, $form['subject'], $headers, $message, $SMTP_CONFIG);
    if (!$result['ok']) {
        $all_ok = false;
        error_log('send-form.php SMTP error (' . $form_id . ' -> ' . $to . '): ' . $result['error']);
    }
}

header('Location: ' . $return_to . (strpos($return_to, '?') === false ? '?' : '&') . 'sent=' . ($all_ok ? '1' : '0') . '#' . $form_id . '-form');
exit;

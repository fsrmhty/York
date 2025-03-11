<?php
// Database configuration
$servername = "sql308.infinityfree.com";
$username = "if0_37528983"; // Change to your database username
$password = "cH97l2BhUUqrMGF";     // Change to your database password
$dbname = "if0_37528983_441week4"; // Change to your database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die(json_encode(['status' => 'error', 'message' => 'Database connection failed.']));
}

// Get input data
$data = json_decode(file_get_contents('php://input'), true);

if (empty($data)) {
    echo json_encode(['status' => 'error', 'message' => 'No data received!']);
    exit;
}

// Insert data into MySQL
$stmt = $conn->prepare("INSERT INTO timetable (subject, day, time, teacher) VALUES (?, ?, ?, ?)");
if (!$stmt) {
    echo json_encode(['status' => 'error', 'message' => 'Prepare failed: ' . $conn->error]);
    exit;
}

foreach ($data as $entry) {
    $subject = $entry['subject'];
    $day = $entry['day'];
    $time = $entry['time'];
    $teacher = $entry['teacher'];

    $stmt->bind_param("ssss", $subject, $day, $time, $teacher);
    if (!$stmt->execute()) {
        echo json_encode(['status' => 'error', 'message' => 'Execute failed: ' . $stmt->error]);
        exit;
    }
}

$stmt->close();
$conn->close();

echo json_encode(['status' => 'success', 'message' => 'Data saved to MySQL successfully!']);
?>
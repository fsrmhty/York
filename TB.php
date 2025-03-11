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
    die("Connection failed: " . $conn->connect_error);
}

// Fetch data from MySQL
$sql = "SELECT subject, day, time, teacher FROM timetable";
$result = $conn->query($sql);

if (!$result) {
    die("Error fetching data: " . $conn->error);
}

// Display data in a table
echo "<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Timetable</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Timetable from MySQL</h1>
    <table>
        <thead>
            <tr>
                <th>Subject</th>
                <th>Day</th>
                <th>Time</th>
                <th>Teacher</th>
            </tr>
        </thead>
        <tbody>";

while ($row = $result->fetch_assoc()) {
    echo "<tr>
            <td>{$row['subject']}</td>
            <td>{$row['day']}</td>
            <td>{$row['time']}</td>
            <td>{$row['teacher']}</td>
          </tr>";
}

echo "</tbody>
    </table>
</body>
</html>";

$conn->close();
?>
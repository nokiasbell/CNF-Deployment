<?php require 'log_header.php'; ?>
<?php
header("content-type:text/html;charset=utf-8");
$pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
$sql = $pdo -> prepare('select * from history where id=?');
$sql -> execute([$_REQUEST['id']]);
foreach($sql->fetchAll() as $row) {
    $status = $row["status"];
    $name = $row["name"];
    $start_time = $row["start_time"];
    $end_time = $row["end_time"];
    $log_file = $row["log_name"];
    $cnf_id = (string)$row["cnf_id"];
}

if ($status=="Started") {
    $log_file = "started.html";
} else {
    foreach ($pdo -> query('select * from cnf where id='.$cnf_id) as $row) {
        $cnf_name = $row['name'];
    }
    $log_file = '../log/'.$cnf_name.'/'.$name.'/'.$log_file;
}

$output = file_get_contents($log_file);
echo "<h1>LOG</h1>";
echo '<p>Result: ',$status,'</p>';
echo '<p>Start Time: ',$start_time,'</p>';
echo '<p>End Time: ',$end_time,'</p>';
echo "<hr>";
echo '<pre>';
echo $output;
echo '</pre>';

?>

<?php require 'log_footer.php'; ?>
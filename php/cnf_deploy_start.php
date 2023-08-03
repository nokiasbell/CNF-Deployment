<?php
date_default_timezone_set('Asia/Shanghai');
$start_time = date("Y-m-d H:i:s");
$end_time = "                   ";
$log_file = "started.html";

$pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');

$row = $pdo -> query('select * from history where status="Started"') -> fetchAll();
if (count($row) >= 1) {
    $url = '/cnf?id='.$_REQUEST['id'];
    if (isset($url))
    {
        Header("Location: $url");
    }
    exit;
}
$sql = $pdo -> prepare('insert into history values(null, "Started", "Deploy", ?, ?, ?,?)');
$sql -> execute([
    $start_time,
    $end_time,
    $log_file,
    $_REQUEST['id']
]);
$url = '/cnf?id='.$_REQUEST['id'];
if (isset($url))
{
    Header("Location: $url");
}
?>
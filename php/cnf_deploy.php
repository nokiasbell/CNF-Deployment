<?php require 'log_header.php'; ?>
<?php
date_default_timezone_set('Asia/Shanghai');
$start_time = date("Y-m-d H:i:s");
$log_file_basename = date("Y-m-d-His").'.html';

$package = $_REQUEST['package'];
$pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
foreach ($pdo -> query('select * from cnf where id='.$_REQUEST['id']) as $row) {
    $cnf_name = $row['name'];
    echo "cnf_name",$cnf_name;
}

$log_file_dir = '../log/'.$cnf_name.'/Deploy/';
mkdir($log_file_dir,0777,true);
$log_file_name = $log_file_dir.$log_file_basename;

system("python ../py/test.py > ".$log_file_name, $re);

$end_time = date("Y-m-d H:i:s");
$sql = $pdo -> prepare('update history set status=?, end_time=?,log_name=? where status="Started"');
if ($re==0) {
    $sql -> execute(['Success',$end_time,$log_file_basename]);
} else {
    $sql -> execute(['Failed',$end_time,$log_file_basename]);
}

?>
<?php require 'log_footer.php'; ?>
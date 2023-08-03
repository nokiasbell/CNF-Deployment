<?php
    date_default_timezone_set('Asia/Shanghai');
    $start_time = date("Y-m-d H:i:s");
    $pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
    $sql = $pdo -> prepare('update cnf set name=?, product=?, ip=?, username=?, password=? where id=?');
    if ($sql -> execute(
        [
            htmlspecialchars($_REQUEST['name']),
            $_REQUEST['product'],
            $_REQUEST['ip'],
            $_REQUEST['username'],
            $_REQUEST['password'],
            $_REQUEST['id']
        ]
    )) {
        echo 'Update CNF Success.';
        $end_time = date("Y-m-d H:i:s");
        $sql = $pdo -> prepare('insert into history values(null, "Success", "Modify", ?, ?, ?)');
        $sql -> execute([$start_time, $end_time, $_REQUEST['id']]);
    } else {
        echo 'Update CNF Failed.';
        $end_time = date("Y-m-d H:i:s");
        $sql = $pdo -> prepare('insert into history values(null, "Failed", "Modify", ?, ?, ?)');
        $sql -> execute([$start_time, $end_time, $_REQUEST['id']]);
    }

    $url = '/cnf?id='.$_REQUEST['id'];
    if (isset($url))
    {
        Header("Location: $url");
    }
?>
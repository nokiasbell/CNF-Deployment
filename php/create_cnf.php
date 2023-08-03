<?php
    $pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
    $sql = $pdo -> prepare('insert into cnf values(null, ?, ?, ?, ?, ?, ?, ?)');
    if ($sql -> execute(
        [
            'NEW',
            htmlspecialchars($_REQUEST['name']),
            $_REQUEST['product'],
            $_REQUEST['tool'],
            $_REQUEST['ip'],
            $_REQUEST['username'],
            $_REQUEST['password']
        ]
    )) {
        echo 'Create CNF Success.';
        $url = '/';
        if (isset($url))
        {
            Header("Location: $url");
        }
    } else {
        echo 'Create CNF Failed.';

    }

?>
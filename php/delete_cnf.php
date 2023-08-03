<?php
    $pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
    $sql = $pdo -> prepare('delete from history where cnf_id=?');
    if ($sql -> execute([$_REQUEST['id']])) {
        echo 'Delete CNF History Success.';
    } else {
        echo 'Delete CNF History Failed.';
    }

    $sql = $pdo -> prepare('delete from cnf where id=?');
    if ($sql -> execute([$_REQUEST['id']])) {
        echo 'Delete CNF Success.';
    } else {
        echo 'Delete CNF Failed.';
    }

    $url = '/';
    if (isset($url))
    {
        Header("Location: $url");
    }
?>
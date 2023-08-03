<?php
    $pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
    $sql1 = $pdo -> prepare('select * from kuafu where id=?');
    $sql1 -> execute([$_REQUEST['id']]);
    $row1 = $sql1 -> fetchAll(); 

    $sql2 = $pdo -> prepare('select * from cnf where tool=?');
    $sql2 -> execute([$row1[0]['version']]);

    $cnf = [];
    $row2 = $sql2 -> fetchAll();
    foreach($row2 as $row) {
        $cnf[] = $row['name']; 
    }
    if ($cnf) {
        echo "Delete Failed.\n" ;
        echo 'Those CNF are using version ',$row1[0]['version'], ': ',implode(', ',$cnf);
    }
    else {
        $sql1 = $pdo -> prepare('delete from kuafu where id=?');
        if ($sql1 -> execute([$_REQUEST['id']])) {
            echo 'Delete Tool Success.';
            $url = '/tool/';
            if (isset($url))
            {
                Header("Location: $url");
            }
        } else {
            echo 'Delete Tool Failed.';
        }
    }
?>
<?php
$os_name = php_uname();
echo $os_name;
if (preg_match("/Windows/", $os_name)) {
    $platform = "windows";
    $target_path = "C:\\Windows\\Temp\\";
} else if (preg_match("/Linux/", $os_name)) {
    $platform = "Linux";
    $target_path = "/tmp/";
}

if ($_FILES['tool']['error'] != UPLOAD_ERR_OK) {
    echo 'Upload File Failed.';
    exit;
}

$target_path = $target_path.basename( $_FILES['tool']['name']);   

if(move_uploaded_file($_FILES['tool']['tmp_name'], $target_path)) {  
    echo "Upload Tool Success.";
} else{  
    echo "Upload Tool Failed.";  
}

if (preg_match("/kuafu-v(\d.\d\d.\d)/", basename( $_FILES['tool']['name']), $match)) {
    $filename = $match[0];
    $version = $match[1];
    $pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
    $sql = $pdo -> prepare('insert into kuafu values(null, ?, ?)');
    if ($sql -> execute(
        [
            htmlspecialchars($filename),
            $version
        ]
    )) {
        echo 'Create Tool Success.';
        $url = '/tool/';
        if (isset($url))
        {
            Header("Location: $url");
        }
    } else {
        echo 'insert tool to db Failed.';
    
    }
} else {
    echo "Create Tool Failed.";
    echo "Please check file name format should match kuafu-v\d.\d\d.\d";
}
?>
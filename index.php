<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Chestnut</title>
    <link rel="shortcut icon" href="img/favicon.ico" type="image/png">
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/font-awesome-4.7.0/css/font-awesome.min.css">
</head>
<body>
    <div class="dialog-wrapper" id="dialog-wrapper">
        <section>
            <header class="dialog-header">
                <h2>Add CNF<a class="dialog-act-close" onclick="close_dialog()"></a></h2>
            </header>
            <form action="/php/create_cnf.php" method="POST">
                <fieldset>
                    <div class="fields">
                        <p class="row">
                            <label for="name">Name:</label>
                            <input type="text" id="name" name="name" class="field-large"  required="required" aria-required="true" autocomplete="off" autofocus />
                        </p>
                        <p class="row">
                            <label for="product">Product:</label>
                            <select id="product" name="product" class="field-large">
                                <option value="VCU">VCU</option>
                                <option value="VDU">VDU</option>
                            </select>
                        </p>
                        <p class="row">
                            <label for="tool">Kuafu Version:</label>
                            <select id="tool" name="tool" class="field-large" required="required">
                            <?php
                                $pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
                                $sql = $pdo -> prepare('select * from kuafu');
                                $sql -> execute();
                                foreach($sql -> fetchAll() as $row) {
                                    echo '<option value="',$row['version'],'">',$row['version'],'</option>';
                                }
                            ?>
                            </select>
                        </p>
                        <p class="row">
                            <label for="ip">OCP SSH IP:</label>
                            <input type="text" id="ip" name="ip" class="field-large" required="required" aria-required="true" autocomplete="off" pattern="\d{1-3}[\.]\d{1-3}[\.]\d{1-3}[\.]\d{1-3}" />
                        </p>
                        <p class="row">
                            <label for="username">Username:</label>
                            <input type="text" id="username" name="username" class="field-large" required="required" autocomplete="off" />
                        </p>
                        <p class="row">
                            <label for="password">Password:</label>
                            <input type="password" id="password" name="password"  class="field-large" required="required" autocomplete="off" />
                        </p>
                    </div>
                </fieldset>
                <footer class="dialog-footer">
                    <input type="submit" value="Confirm" class="dialog-act-submit" />        
                </footer>
            </form>
        </section>
    </div>

    <div class="page">
        <header class="masthead">
            <a class="btn-function" onclick="open_sidebar()" id="btn-func-list"></a>
            <p class="logo"><a href="/"><img src="/img/favicon.ico" alt="chestnut ico"></a></p>
            <h1 class="subject">CNF Deployment</h1>
        </header>

        <main>
            <div class="main-header">
                <h2>Cloud Network Function</h2>
                <a onclick="open_dialog()" title="New CNF"></a>
            </div>
            <form action="/" method="POST">
                <div class="search-wapper">
                    <label for="search"></label>
                    <?php
                        if (isset($_REQUEST['search'])) {
                            echo '<input class="btn-search" type="search" id="search" name="search" placeholder="search name..." autocomplete="off" value="', $_REQUEST['search'],'">';
                        } else {
                            echo '<input class="btn-search" type="search" id="search" name="search" placeholder="search name..." autocomplete="off">';
                        }
                    ?>
                </div>
            </form>
            <article class="table-header">
                <div>status</div>
                <div>name</div>
                <div>product</div>
                <div>ip</div>
                <div>kuafu</div>
                <div style="visibility: hidden">operation</div>
            </article>
            <?php
                $pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
                if (isset($_REQUEST['search'])) {
                    $sql = $pdo -> prepare('select * from cnf where name like ?');
                    $sql -> execute(['%'.$_REQUEST['search'].'%']);
                } else {
                    $sql = $pdo -> prepare('select * from cnf');
                    $sql -> execute();
                }
                foreach($sql -> fetchAll() as $row) {
                    echo '<article class="table-row">';
                    echo '<div>', $row['status'],'</div>';
                    echo '<div><a href="/cnf/?id=', $row['id'],'">', $row['name'],'</a></div>';
                    echo '<div>',$row['product'],'</div>';
                    echo '<div>',$row['ip'],'</div>';
                    echo '<div>',$row['tool'],'</div>';
                    echo '<div class="op-btn-group">';
                    echo '<a class="btn-conf" href="/cnf/?id=', $row['id'] ,'"></a>';
                    echo '<a class="btn-del" href="/php/delete_cnf.php?id=', $row['id'] ,'"></a>';
                    echo '</div>';
                    echo '</article>';
                }
            ?>
            <!-- <article class="table-row">
                <div>installed</div>
                <div><a href="cnf/index.html">TL-10944</a></div>
                <div>VCU</div>
                <div>10.68.169.10</div>
                <div>
                    <button class="btn-conf"></button>
                    <button class="btn-del"></button>
                </div>
            </article> -->
        </main>
        <div class="sidebar-wrapper" id="sidebar-wrapper">
            <div class="sidebar" id="sidebar">
                <aside>
                    <ul class="menu">
                        <li><a href="/tool/">Kuafu Tool</a></li>
                        <li><a href="/">CNF</a></li>
                    </ul>
                </aside>                
            </div>
        </div>
        <footer>
            <small>&copy;Copyright Nokia</small>
        </footer>
    </div>

<script src="/js/script.js"></script>

</body>
</html>
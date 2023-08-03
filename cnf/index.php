<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Chestnut</title>
    <link rel="shortcut icon" href="/img/favicon.ico" type="image/png">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/detail.css">
    <link rel="stylesheet" href="/css/font-awesome-4.7.0/css/font-awesome.min.css">
</head>
<body>
    <div class="workbench-wrapper" id="workbench-modify">
        <section>
            <header class="workbench-header">
                <h4>Modify CNF</h4>
            </header>
            <form action="/php/cnf_modify.php" method="POST">
                <fieldset>
                    <div class="wb-fields">
                        <p class="wb-row wb-row-header">
                            <label>key</label>
                            <label>value</label>
                        </p>
                        <?php
                            if (isset($_REQUEST['id'])) {
                                $pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
                                $sql = $pdo -> prepare('select * from cnf where id=?');
                                $sql -> execute([$_REQUEST['id']]);
                                foreach($sql -> fetchAll() as $row) {
                                    echo '<input type="hidden" name="id" value="', $row['id'],'">';

                                    echo '<p class="wb-row">';
                                    echo '<label for="name">Name:</label>';
                                    echo '<input type="text" id="name" name="name" class="field-large"  required="required" aria-required="true" autocomplete="off" autofocus value="', $row['name'], '">';
                                    echo '</p>';

                                    echo '<p class="wb-row">';
                                    echo '<label for="product">Product:</label>';
                                    echo '<select id="product" name="product" class="field-large" value="', $row['product'] ,'">';
                                    echo '<option value="VCU">VCU</option>';
                                    echo '<option value="VDU">VDU</option>';
                                    echo '</select>';
                                    echo '</p>';

                                    echo '<p class="wb-row">';
                                    echo '<label for="ip">OCP SSH IP:</label>';
                                    echo '<input type="text" id="ip" name="ip" class="field-large" required="required" aria-required="true" autocomplete="off" pattern="\d{1-3}[\.]\d{1-3}[\.]\d{1-3}[\.]\d{1-3}" value="', $row['ip'], '">';
                                    echo '</p>';

                                    echo '<p class="wb-row">';
                                    echo '<label for="username">Username:</label>';
                                    echo '<input type="text" id="username" name="username" class="field-large" required="required" autocomplete="off" value="', $row['username'], '">';
                                    echo '</p>';

                                    echo '<p class="wb-row">';
                                    echo '<label for="password">Password:</label>';
                                    echo '<input type="password" id="password" name="password"  class="field-large" required="required" autocomplete="off" value="', $row['password'],'">';
                                    echo '</p>';
                                }
                            }
                        ?>
                        <!-- <p class="wb-row">
                            <label for="name">Name:</label>
                            <input type="text" id="name" name="name" class="field-large"  required="required" aria-required="true" autocomplete="off" autofocus />
                        </p>
                        <p class="wb-row">
                            <label for="product">Product:</label>
                            <select id="product" name="product" class="field-large">
                                <option value="vcu">VCU</option>
                                <option value="vdu">VDU</option>
                            </select>
                        </p>
                        <p class="wb-row">
                            <label for="ip">OCP SSH IP:</label>
                            <input type="text" id="ip" name="ip" class="field-large" required="required" aria-required="true" autocomplete="off" pattern="\d{1-3}[\.]\d{1-3}[\.]\d{1-3}[\.]\d{1-3}" />
                        </p>
                        <p class="wb-row">
                            <label for="username">Username:</label>
                            <input type="text" id="username" name="username" class="field-large" autocomplete="off" />
                        </p>
                        <p class="wb-row">
                            <label for="password">Password:</label>
                            <input type="password" id="password" name="password"  class="field-large" autocomplete="off" />
                        </p> -->
                    </div>
                </fieldset>
                <footer class="workbench-footer">
                    <?php
                        if (isset($_REQUEST['id'])) {
                            echo '<a class="wb-btn-cancel" href="/cnf/?id=', $_REQUEST['id'],'">Cancel<a>';
                            echo '<input type="submit" value="Confirm" class="wb-btn-submit" />';      
                        }
                    ?>
                </footer>
            </form>
        </section>
    </div>
    <div class="workbench-wrapper" id="workbench-deploy">
        <section>
            <header class="workbench-header">
                <h4>Deploy CNF</h4>
            </header>
            <form id="form-deploy" action="/php/cnf_deploy_start.php" method="GET">
                <fieldset>
                    <div class="wb-fields">
                        <p class="wb-row">
                            <?php
                                if (isset($_REQUEST['id'])) {
                                    echo '<input type="hidden" name="id" value="', $_REQUEST['id'],'">';
                                }
                            ?>
                            <label for="package">Package Name:</label>
                            <input type="text" id="package" name="package" class="field-large" autocomplete="off" />
                        </p>
                    </div>
                </fieldset>
                <footer class="workbench-footer">
                    <?php
                        if (isset($_REQUEST['id'])) {
                            echo '<a class="wb-btn-cancel" href="/cnf/?id=', $_REQUEST['id'],'">Cancel<a>';
                            echo '<input type="button" value="Confirm" class="wb-btn-submit" onclick="getNewContent()"/>';      
                        }
                    ?>
                </footer>
            </form>
        </section>
    </div>
    <div class="page">
        <header class="masthead">
            <a class="btn-function" onclick="open_sidebar()" id="btn-func-list"></a>
            <p class="logo"><a href="/"><img src="../img/favicon.ico" alt="chestnut ico"></a></p>
            <h1 class="subject">CNF Deployment</h1>
        </header>

        <main>
            <div class="main-header">
                <h2>Cloud Network Function Detail</h2>
            </div>
                <article class="property">
                    <h3>PROPERTY</h3>
                    <?php
                        if (isset($_REQUEST['id'])) {
                            $pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
                            $sql = $pdo -> prepare('select * from cnf where id=?');
                            $sql -> execute([$_REQUEST['id']]);
                            foreach($sql -> fetchAll() as $row) {
                                echo '<section>';
                                echo '<label for="status-value">Status</label>';
                                echo '<input id="status-value" value="', $row['status'] ,'">';
                                echo '</section>';
                                echo '<section>';
                                echo '<label for="name-value">Name</label>';
                                echo '<input id="name-value" value="', $row['name'] ,'">';
                                echo '</section>';
                                echo '<section>';
                                echo '<label for="product-value">Product</label>';
                                echo '<input id="product-value" value="', $row['product'] ,'">';
                                echo '</section>';
                                echo '<section>';
                                echo '<label for="ip-value">SSH IP</label>';
                                echo '<input id="ip-value" value="', $row['ip'] ,'">';
                                echo '</section>';
                                echo '<section>';
                                echo '<label for="tool-value">Kuafu Version</label>';
                                echo '<input id="tool-value" value="', $row['tool'] ,'">';
                                echo '</section>';                            
                            }
                        }
                    ?>
                    <!-- <section class="item">
                        <label for="name-value">Name</label>
                        <input id="name-value" value="VCU-10944">
                    </section>
                    <section class="item">
                        <label for="product-value">Product</label>
                        <input id="product-value" value="VCU">
                    </section>
                    <section class="item">
                        <label for="ip-value">SSH IP</label>
                        <input id="ip-value" value="1.1.1.1">                    
                    </section>
                    <section class="item">
                        <label for="tool-value">Tool Version</label>
                        <input id="tool-value" value="kuafu-v6.19.0">
                    </section> -->
                </article>                
                
                <article class="operation">
                    <h3>OPERATIONS</h3>
                        <section>
                            <h4>CNF Operation</h4>
                            <p><a onclick="display_workbench_modify()">Modify</a></p>
                        </section>
                        <section>
                            <h4>Standard Operation</h4>
                            <p><a>Config</a></p>
                            <p><a>Onboard</a></p>
                            <p><a onclick="display_workbench_deployment()">Deployment</a></p>
                        </section>
                        <section>
                            <h4>Other Operation</h4>
                            <p><a>Config</a></p>
                        </section>
                </article>
                <div class="history">
                    <h3>HISTORY</h3>
                    <article class="table-header">
                        <div>status</div>
                        <div>operation</div>
                        <div>started</div>
                        <div>finished</div>
                    </article>
                    <?php
                        if (isset($_REQUEST['id'])) {
                            $pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
                            $sql = $pdo -> prepare('select * from history where cnf_id=?');
                            $sql -> execute([$_REQUEST['id']]);
                            foreach($sql -> fetchAll() as $row) {
                                echo '<article class="table-row">';
                                echo '<div>', $row['status'], '</div>';
                                echo '<div><a href="/php/display_log.php?id=',$row['id'],'">', $row['name'], '</a></div>';
                                echo '<div>',$row['start_time'],'</div>';
                                echo '<div>',$row['end_time'],'</div>';
                                echo '</article>';
                            }
                        }
                    ?>
                    <!-- <article class="table-row">
                        <div>installed</div>
                        <div><a href="cnf/index.html">Modify</a></div>
                        <div>2022-09-30 13:19:39</div>
                        <div>2022-09-30 13:40:39</div>
                    </article> -->
                </div>
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
    </div>
    <script src="/js/script.js"></script>
    <script src="/js/addLoadEvent.js"></script>
    <script src="/js/getNewContent.js"></script>
</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Chestnut</title>
    <link rel="shortcut icon" href="/img/favicon.ico" type="image/png">
    <link rel="stylesheet" href="/css/main.css">
    <link rel="stylesheet" href="/css/font-awesome-4.7.0/css/font-awesome.min.css">
</head>
<body>
    <div class="dialog-wrapper" id="dialog-wrapper">
        <section>
            <header class="dialog-header">
                <h2>Add Kuafu Tool <a class="dialog-act-close" onclick="close_dialog()"></a></h2>
            </header>
            <form action="/php/create_tool.php" method="POST" enctype="multipart/form-data">
                <fieldset class="file">
                    <div class="fields">
                        <br class="row">
                            <label for="tool">Tool Path:</label>
                            <input type="file" id="tool" name="tool" class="field-large"  required="required" aria-required="true"  />
                            <aside class="dialog-notes">
                                <small>
                                    *Name format must be kuafu-v<cite>X.XX.X.tar.gz </cite>(X is number)
                                </small>
                            </aside>
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
            <p class="logo"><a href="/"><img src="../img/favicon.ico" alt="chestnut ico"></a></p>
            <h1 class="subject">CNF Deployment</h1>
        </header>
        <main>
            <div class="main-header">
                <h2>Kuafu Tool</h2>
                <a onclick="open_dialog()" title="Add Kuafu Tool"></a>
            </div>
            <article class="table-header">
                <div>name</div>
                <div>version</div>
                <div style="visibility: hidden">operation</div>
            </article>
            <?php
                $pdo = new PDO('mysql:host=localhost;dbname=db;charset=utf8','staff','password');
                $sql = $pdo -> prepare('select * from kuafu');
                $sql -> execute();
                foreach($sql -> fetchAll() as $row) {
                    echo '<article class="table-row">';
                    echo '<div>',$row['name'],'</div>';
                    echo '<div>',$row['version'],'</div>';
                    echo '<div class="op-btn-group">';
                    echo '<a class="btn-del" href="/php/delete_tool.php?id=', $row['id'],'"></a>';
                    echo '</div>';
                    echo '</article>';
                }
            ?>
            <!-- <article class="table-row">
                <div>kuafu-v6.19.0</div>
                <div>6.19.0</div>
                <div>
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

<script src="/js/script.js">
</script>

</body>
</html>
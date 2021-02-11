<!DOCTYPE php>
<html>
<head>
    <title>Search!</title>
</head>

<body>
    
    <h1 style="text-align:center; padding-top:20px; padding-bottom:10px">
        Search!
    </h1>
    <form style="text-align:center; padding-bottom:20px" action="query.php" method="post">
        <input type="text" name="search_query"><br>
        <input type="submit" value="Search!">
    </form>

    <?php
        $servername = "HOST_NAME";
        $username = "USER_NAME";
        $password = "USER_PASSWORD";
        $database = "DATABASE_NAME";

        // Create connection
        $conn = new mysqli($servername, $username, $password, $database);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $query = $_POST["search_query"];

        $sql = "SELECT * FROM websites WHERE title COLLATE UTF8_GENERAL_CI LIKE '%$query%' UNION SELECT * FROM websites WHERE url COLLATE UTF8_GENERAL_CI LIKE '%$query%' UNION SELECT * FROM websites WHERE keywords COLLATE UTF8_GENERAL_CI LIKE '%$query%'";
        $result = $conn->query($sql);

        $count = 0;

        $result_array = array();

        if ($result->num_rows > 0) {

            while($row = $result->fetch_assoc() and $count < 100) {
                array_push($result_array, $row);
                $count += 1;
            }

            foreach ($result_array as $row) {
                echo "<div>" . $row["title"]. "<br> <a href=http://" . $row["url"] . "> http://" . $row["url"]. "</a></div><br>";
            }

        } else {
            echo "<div>No Results</div>";
        }

    ?>

</body>

</html>
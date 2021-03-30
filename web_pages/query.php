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
                $sql2 = "SELECT to_url, COUNT(to_url) as 'c' FROM connections WHERE to_url = '" . $row["url"] . "' GROUP BY to_url";
                $result2 = $conn->query($sql2);
                $row["c"] = $result2->fetch_row()[1];
                array_push($result_array, $row);
                $count += 1;
            }
            
            usort($result_array, function($a, $b) {
                return $b['c'] <=> $a['c'];
            });
            
            foreach ($result_array as $row) {
                echo "<div>" . $row["title"]. "<br> <a class='result_link' href=http://" . $row["url"] . "> http://" . $row["url"]. "</a></div><br>";
            }

        } else {
            echo "<div>No Results</div>";
        }

    ?>

</body>

</html>

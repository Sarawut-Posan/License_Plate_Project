<?php
/* Attempt MySQL server connection. Assuming you are running MySQL
server with default setting (user 'root' with no password) */
$link = mysqli_connect("jassada.cdqqutbe7d4o.us-east-2.rds.amazonaws.com", "root", "taaisasvmw45120", "LPR");
 
// Check connection
if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
 
// Attempt select query execution
$sql = "SELECT * FROM lpr_name";
if($result = mysqli_query($link, $sql)){
    if(mysqli_num_rows($result) > 0){
        echo "<table>";
            echo "<tr>";
                echo "<th>dates</th>";
                echo "<th>times</th>";
                echo "<th>city</th>";
                echo "<th>number</th>";
                echo "<th>top part file</th>";
            echo "</tr>";
        while($row = mysqli_fetch_array($result)){
            echo "<tr>";
                echo "<td>" . $row['dates'] . "</td>";
                echo "<td>" . $row['times'] . "</td>";
                echo "<td>" . $row['city'] . "</td>";
                echo "<td>" . $row['number'] . "</td>";
                echo "<td>" . $row['top_part_file'] . "</td>";
            echo "</tr>";
        }
        echo "</table>";
        // Free result set
        mysqli_free_result($result);
    } else{
        echo "No records matching your query were found.";
    }
} else{
    echo "ERROR: Could not able to execute $sql. " . mysqli_error($link);
}
 
// Close connection
mysqli_close($link);
?>
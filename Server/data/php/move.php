<?php
session_start();

function sendRequest($data)
{
    $url = $_ENV["URL"];
    $jsondata = json_encode($data);
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $jsondata);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Accept: application/json', 'Content-Type: application/json'));

    $result = curl_exec($ch);
    $resulj = json_decode($result);
    curl_close($ch);

    return $resulj->action;
}


function FindBlank($state)
{
    $rows = $cols = 4;
    for ($row = 0; $row < $rows; $row++) {
        for ($col = 0; $col < $cols; $col++) {
            if ($state[$row][$col] == 0)
                return array($row, $col);
        }
    }
}
function moved($action, $state, $error)
{
    $aState = FindBlank($state);
    $BlankRow = $aState[0];
    $BlankCol = $aState[1];
    $cols = $rows = 4;
    switch ($action) {
        case "Up":
            if ($BlankRow == 0) {
                $error = true;
                break;
            }
            $tmp = $state[$BlankRow][$BlankCol];
            $state[$BlankRow][$BlankCol] = $state[$BlankRow - 1][$BlankCol];
            $state[$BlankRow - 1][$BlankCol] = $tmp;
            break;
        case "Down":
            if ($BlankRow == $rows - 1) {
                $error = true;
                break;
            }
            $tmp = $state[$BlankRow][$BlankCol];
            $state[$BlankRow][$BlankCol] = $state[$BlankRow + 1][$BlankCol];
            $state[$BlankRow + 1][$BlankCol] = $tmp;
            break;
        case "Right":
            if ($BlankCol == $cols - 1) {

                $error = true;
                break;
            }
            $tmp = $state[$BlankRow][$BlankCol];
            $state[$BlankRow][$BlankCol] = $state[$BlankRow][$BlankCol + 1];
            $state[$BlankRow][$BlankCol + 1] = $tmp;
            break;
        case "Left":
            if ($BlankCol == 0) {
                $error = true;
                break;
            }
            $tmp = $state[$BlankRow][$BlankCol];
            $state[$BlankRow][$BlankCol] = $state[$BlankRow][$BlankCol - 1];
            $state[$BlankRow][$BlankCol - 1] = $tmp;
            break;
        case "None":
            $data = array(
                'state' => $state
            );
            $newAction = sendRequest($data);

            $state = moved($newAction, $state, $error)[0];
            break;
    }

    return $resultAry = array($state, $error);
}


//--------------------------------------------------------------------------------------
$data = json_decode(file_get_contents('php://input'));
$action = $data->action;
$state = $data->state;
$error = false;
//클라이언트로부터 데이터 받아서 각 변수에 저장

$state = moved($action, $state, $error)[0]; //moving 함수로 state값 변경
$error = moved($action, $state, $error)[1];

if (!isset($_SESSION['count']))
    $_SESSION['count'] = 0;
else $_SESSION['count']++; //stringArray의 인덱스값 형성

for ($i = 0; $i < 4; $i++) {
    $stringState[$i] = implode("/", $state[$i]); //state값을 문자열로 변환
}
$stringAry[$_SESSION['count']] = $stringState[0] . "/" . $stringState[1] . "/" . $stringState[2] . "/" . $stringState[3];
//배열저장이 안되므로 문자열로 변환후 저장
if (!isset($_SESSION['compare'])) {
    $_SESSION['compare'] = "";
} //저장하고 비교할 세션 문자열

if (strpos($_SESSION['compare'], "#" . $stringAry[$_SESSION['count']]) !== false)
    $error = true;
//session값에 저장되어 있는 문자열과 비교

$_SESSION['compare'] = $_SESSION['compare'] . "#" . $stringAry[$_SESSION['count']];
//session변수에 array의 문자열값 저장.

if ($error == true) {
    session_destroy();
}
$data->state = $state;
$data->error = $error;
$data->action = $action;

print(json_encode($data));//값 반환

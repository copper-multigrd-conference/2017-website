// (c) 2014-2015 easychair.org
var selectedLetter;
function selectLetter(anchor)
{
    if (selectedLetter) {
        document.getElementById(selectedLetter).className = "letter";
    }
    document.getElementById(anchor).className = "letter_sel";
    selectedLetter = anchor;
    return true;
}
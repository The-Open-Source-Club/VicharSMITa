var main = {
    searchbarClicked : false,
    menuButtonClicked: false,
}

function searchbar()
{
    if(!main.searchbarClicked)
    {
        document.getElementById("main-searchbar").value = "";
        main.searchbarClicked = true;
    }
}

function menu()
{
    if(!main.menuButtonClicked)
    {
        console.log("1");
        document.getElementById("main-menu").style.right = 0;
        main.menuButtonClicked = true;
    }
    else
    {
        console.log("2");
        document.getElementById("main-menu").style.right = "-320px";
        main.menuButtonClicked = false;
    }
}

function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1);
};

if (isMobileDevice() == true){
    document.getElementById('game_panel_table').setAttribute('height', 0.85*window.innerHeight);
    document.getElementById('game_panel_table').setAttribute('width', 0.95*window.innerWidth);
        if (window.innerHeight<window.innerWidth){
            document.getElementById('game_panel_table').style.fontSize = "75%";
        }
        else document.getElementById('game_panel_table').style.fontSize = "90%";
}
else {
    document.getElementById('game_panel_table').setAttribute('height', 0.85*window.innerHeight);
    document.getElementById('game_panel_table').setAttribute('width', 0.95*window.innerWidth);
    document.getElementById('game_panel_table').style.fontSize = "90%";
}
document.getElementById('game_panel_table').style.fontSize = "90%";

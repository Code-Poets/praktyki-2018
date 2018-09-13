function getCookie(name)
{
    var start = document.cookie.indexOf( name + "=" );
    var len = start + name.length + 1;
    if ( ( !start ) && ( name != document.cookie.substring( 0, name.length ) ) ) {
        return null;
    }
    if ( start == -1 ) return null;
    var end = document.cookie.indexOf( ";", len );
    if ( end == -1 ) end = document.cookie.length;
    return unescape( document.cookie.substring( len, end ) );
}

function doload()
{
    var scrollTop = getCookie ("scrollTop");
    var scrollLeft = getCookie("scrollLeft");

    if (!isNaN(scrollTop))
    {
      document.body.scrollTop = scrollTop;
      document.documentElement.scrollTop = scrollTop;

    }
    if (!isNaN(scrollLeft))
    {
          document.body.scrollLeft = scrollLeft;
          document.documentElement.scrollLeft = scrollLeft;
    }

    Delete_Cookie("scrollTop");
    Delete_Cookie("scrollLeft");
    setTimeout( "Refresh()", 10000 );
}

function Refresh()
{
    document.cookie = 'scrollTop=' + f_scrollTop();
    document.cookie = 'scrollLeft=' + f_scrollLeft();
    document.location.reload(true);
}

//Setting the cookie for vertical position
function f_scrollTop() {
    return f_filterResults (
        window.pageYOffset ? window.pageYOffset : 0,
        document.documentElement ? document.documentElement.scrollTop : 0,
        document.body ? document.body.scrollTop : 0
    );
}

function f_filterResults(n_win, n_docel, n_body) {
    var n_result = n_win ? n_win : 0;
    if (n_docel && (!n_result || (n_result > n_docel)))
        n_result = n_docel;
    return n_body && (!n_result || (n_result > n_body)) ? n_body : n_result;
}

//Setting the cookie for horizontal position
function f_scrollLeft() {
    return f_filterResults (
        window.pageXOffset ? window.pageXOffset : 0,
        document.documentElement ? document.documentElement.scrollLeft : 0,
        document.body ? document.body.scrollLeft : 0
    );
}

function Delete_Cookie(name)
{
    document.cookie = name + "=" + ";expires=Thu, 01-Jan-1970 00:00:01 GMT";

}

window.onload=doload;

function increment(incrementor, target){
    var value = parseInt(document.getElementById(target).value);
    value+=incrementor;
    document.getElementById(target).value = value;
};

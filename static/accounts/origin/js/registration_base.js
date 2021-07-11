
// registration background theme
var nodesjs = new NodesJs({
    id: 'nodes',
    width: document.getElementsByClassName('registration-bg')[0].clientWidth,
    height: document.getElementsByClassName('registration-bg')[0].clientHeight,
    particleSize: 2,
    lineSize: 1,
    particleColor: [22, 46, 137, 0.3],
    lineColor: [0, 186, 241],
    backgroundFrom: [255, 255, 255],
    backgroundTo: [255, 255, 255],
    backgroundDuration: 4000,
    nobg: false,
    number: Math.round((35 / 1100) * document.getElementsByClassName('registration-bg')[0].clientWidth,0), //window.hasOwnProperty('orientation') ? 30: 100,
    speed: 10
});
window.onresize = function () {
    nodesjs.setWidth(document.getElementsByClassName('registration-bg')[0].clientWidth);
    nodesjs.setHeight(document.getElementsByClassName('registration-bg')[0].clientHeight);
};
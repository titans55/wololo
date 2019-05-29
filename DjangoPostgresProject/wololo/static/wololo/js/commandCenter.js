var isVillageSelected = false;
var infos = JSON.parse($('.map-data').attr('map-data'))
var selectedVillage = JSON.parse(($('.selected-village').attr('data')).replace(/'/g, '"'))

var winW = document.body.offsetWidth;
var winH = document.body.offsetHeight;

game = new Phaser.Game(winW / 2, winH / 3 * 2, Phaser.AUTO, 'game-container', { preload: preload, create: create, update: update });

function preload() {
    game.scale.scaleMode = Phaser.ScaleManager.USER_SCALE;
    game.load.image("tiles", " http://localhost:8000/static/wololo/mapAssets/tilesets/overworld_tileset_grass.png");
    game.load.tilemap('map', ' http://localhost:8000/static/wololo/mapAssets/tilemaps/mapv3.json', null, Phaser.Tilemap.TILED_JSON);
    game.load.spritesheet('castle', ' http://localhost:8000/static/wololo/mapAssets/sprites/castle.png', { frameWidth: 48, frameHeight: 48 });
    game.load.spritesheet('pathDot', ' http://localhost:8000/static/wololo/mapAssets/sprites/pathDot.png', { frameWidth: 16, frameHeight: 16 });
    game.load.spritesheet('selected', ' http://localhost:8000/static/wololo/mapAssets/sprites/selection-circle_1_64x64.png', { frameWidth: 64, frameHeight: 64 });
}

function create() {
    createMap();
    loadVillages(infos);
    $("#game-container").remove()
    initTargetSelection()


}

function update(time, delta) {

}

function createMap() {
    map = game.add.tilemap('map');
    const tileset = map.addTilesetImage("Tile", "tiles");
    groundLayer = map.createLayer('groundLayer');
    groundLayer.resizeWorld();
    seaLayer = map.createLayer('seaLayer');
    // collision layer
    collision_tiles = [];
    seaLayer.layer.data.forEach(function (data_row) { // find tiles used in the layer
        data_row.forEach(function (tile) {
            // check if it's a valid tile index and isn't already in the list
            if (tile.index > 0 && collision_tiles.indexOf(tile.index) === -1) {
                collision_tiles.push(tile.index);
            }
        }, this);
    }, this);
    map.setCollision(collision_tiles, true, seaLayer.layer.name);
    // console.log(collision_tiles, "bababa")    
    seaLayer.resizeWorld();
}

function loadVillages(infos) {
    var sprite
    tile_dimensions = new Phaser.Point(map.tileWidth, map.tileHeight);
    pathfinding = this.game.plugins.add(PathfindingExample.Pathfinding, map.layers[1].data, [-1], tile_dimensions);
    infos.forEach(function(element) {
        if(element.playerName != ''){
            sprite = game.add.sprite(element.coords.x, element.coords.y, 'castle');
            sprite.village_id = element.village_id;
            sprite.user_id = element.user_id;
            sprite.owner = element.owner ? 'yours' : ''
            sprite.villageName = element.villageName;
            sprite.playerName = element.playerName;
            sprite.villagePoints = element.points
            sprite.village_id = element.village_id
            sprite.player_id = element.user_id
            sprite.x = element.coords.x;
            sprite.y = element.coords.y;
            sprite.inputEnabled = true;
        }
    })
}

function initTargetSelection(){
    var targetVillageData = JSON.parse(($("#targetVillageData").attr("data")).replace(/'/g, '"'))
    let target_position = new Phaser.Point(targetVillageData.coords.x, targetVillageData.coords.y)
    let from = new Phaser.Point(selectedVillage.coords.x, selectedVillage.coords.y)
    pathfinding.find_path(from, target_position, this.move_through_path, this)  
}

function makeChangesForCommandCenterInPathfindingJS(){ //called in PathFinding.js
    $("#distance").html(pathLength)

    listenTroopsToTrainInputChange()
    initInVillageTroopMarker()
}

function listenTroopsToTrainInputChange(){
    $(".troopsToSend").on('change',function(){
        if($(this).val()>parseInt($(this).attr("max"))) $(this).val(parseInt($(this).attr("max")))
        let slowestUnitSpeed = getSpeedOfSlowestUnitAndUpdateTroopsFormInput() // pathPerMin
        let estimatedTime = pathLength / slowestUnitSpeed //minutes
        console.log(slowestUnitSpeed, " => slowestUnitSpeed")
        console.log(estimatedTime, " minutes => estimatedTime")
        $(".estimatedMinutes-form-input").val(estimatedTime)
    })
}

function getSpeedOfSlowestUnitAndUpdateTroopsFormInput(){
    let slowestSpeed = Number.POSITIVE_INFINITY
    let troopsToSend = {
        "infantry": {
            "Spearman" : 0,
            "Swordsman" : 0,
            "Axeman" : 0,
            "Archer" : 0
        },
        "cavalry" : {
            "Scout" : 0,
            "Light Cavalry": 0,
            "Heavy Cavalry" : 0
        },
        "siegeWeapons" : {
            "Ram" : 0,
            "Catapult": 0
        }
    }
    $(".troopsToSend").each(function(){
        if(parseInt($(this).val())>0){
            const unitType = $(this).attr("unitType")
            const unitName = $(this).attr("unitName")
            let speedOfUnit = gameConfigs.units[unitType][unitName].speed
            if(speedOfUnit<slowestSpeed) slowestSpeed = speedOfUnit

            troopsToSend[unitType][unitName] = parseInt($(this).val())
        }
    })
    $(".troops-form-input").val(JSON.stringify(troopsToSend))
    return slowestSpeed
}

function initInVillageTroopMarker(){
    $(".inVillageTroopMarker").not(".disabled").on("click", function(){
        console.log($(this), " wololo")
        let totalAmount = parseInt($(this).find(".troopAmount").html())
        $(this).siblings(".troopsToSend").val(totalAmount).change();
    })
}
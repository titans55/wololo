var isVillageSelected = false;
var infos = JSON.parse($('.map-data').attr('map-data'))
var selectedVillage = JSON.parse(($('.selected-village').attr('data')).replace(/'/g, '"'))

var winW = document.body.offsetWidth;
var winH = document.body.offsetHeight;
var pathfinding

game = new Phaser.Game(winW / 2, winH / 3 * 2, Phaser.AUTO, 'game-container', { preload: preload, create: create, update: update });

function preload() {
    game.scale.scaleMode = Phaser.ScaleManager.USER_SCALE;
    // game.load.image("tiles", "../static/wololo/mapAssets/tilesets/overworld_tileset_grass.png");
    // game.load.tilemap('map', '../static/wololo/mapAssets/tilemaps/mapv3.json', null, Phaser.Tilemap.TILED_JSON);
    // game.load.spritesheet('castle', '../static/wololo/mapAssets/sprites/castle.png', { frameWidth: 48, frameHeight: 48 });
    // game.load.spritesheet('pathDot', '../static/wololo/mapAssets/sprites/pathDot.png', { frameWidth: 16, frameHeight: 16 });
    // game.load.spritesheet('selected', '../static/wololo/mapAssets/sprites/selection-circle_1_64x64.png', { frameWidth: 64, frameHeight: 64 });
    game.load.image("tiles", " http://localhost:8000/static/wololo/mapAssets/tilesets/overworld_tileset_grass.png");
    game.load.tilemap('map', ' http://localhost:8000/static/wololo/mapAssets/tilemaps/mapv3.json', null, Phaser.Tilemap.TILED_JSON);
    const spriteRoot = 'http://localhost:8000/static/wololo/mapAssets/sprites/'
    
    game.load.spritesheet('tr1', spriteRoot + 'cultures/turkish/on.png', { frameWidth: 48, frameHeight: 48 });
    game.load.spritesheet('tr2', spriteRoot + 'cultures/turkish/2.png', { frameWidth: 48, frameHeight: 48 });
    game.load.spritesheet('castle', spriteRoot + 'castle.png', { frameWidth: 48, frameHeight: 48 });
    game.load.spritesheet('pathDot', spriteRoot + 'pathDot.png', { frameWidth: 16, frameHeight: 16 });
    game.load.spritesheet('selected', spriteRoot + 'selection-circle_1_64x64.png', { frameWidth: 64, frameHeight: 64 });
}

function create() {
    createMap();
    loadVillages(infos);
    initSwitchVillage()
}

function update(time, delta) {
    drag();
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
    infos.forEach(function(element) {
        if(element.playerName != ''){
            let villageImage;
            if(element.villagePoints>200){
                villageImage = 'tr2'
            }else{
                villageImage = 'tr1'
            }

            sprite = game.add.sprite(element.coords.x, element.coords.y, villageImage);
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
            sprite.events.onInputDown.add(onClickListener, sprite);
            sprite.events.onInputOver.add(onHoverListener, sprite);
            sprite.events.onInputOut.add(onOutListener, sprite);
        }
    })
}

function onClickListener(sprite) {
    console.log(selectedVillage)
    targetVilCoords = {
        'x' : sprite.x,
        'y' : sprite.y
    }
    
    if (isVillageSelected) {
        console.log(selectedIndicator)
        selectedIndicator.kill();
        isVillageSelected = false;
        selectedIndicator = game.add.sprite(sprite.x - 10, sprite.y - 8, 'selected');
        isVillageSelected = true;
        initSideBar(sprite)
        removePathSprites()
        if(!sprite.owner){
            findPath(selectedVillage.coords, targetVilCoords)
        }

    }else{
        selectedIndicator = game.add.sprite(sprite.x - 10, sprite.y - 8, 'selected');
        isVillageSelected = true;
        initSideBar(sprite)

        if(!sprite.owner){
            findPath(selectedVillage.coords, targetVilCoords)
        }
    }
}

function onHoverListener(sprite, event) {
    document.body.style.cursor = "pointer";

    let mousePositionX = event.pageX;
    let mousePositionY = event.pageY;
    $('#tooltip span').html(sprite.playerName + "<br>" + sprite.villageName + "<br>" + sprite.owner);
    $('#tooltip').stop(false, true).fadeIn(1000);
    $('#tooltip').css({ 'top': mousePositionY - winH / 18, 'left': mousePositionX - winW / 40 + 40 });


    var tooltip = document.querySelectorAll('#tooltip');

    function fn(e) {
        for (var i=tooltip.length; i--;) {
            tooltip[i].style.left = e.pageX + 'px';
            tooltip[i].style.top = e.pageY + 'px';
        }
    }

    document.addEventListener('mousemove', fn, false);

}

function onOutListener(sprite) {
    $('#tooltip').stop(false, true).fadeOut(0);

    document.body.style.cursor = "default";

}

function drag() {
    if (game.input.activePointer.isDown) {
        if (game.origDragPoint) { // move the camera by the amount the mouse has moved since last update
            game.camera.x += game.origDragPoint.x - game.input.activePointer.position.x;
            game.camera.y += game.origDragPoint.y - game.input.activePointer.position.y;
        } // set new drag origin to current position
        game.origDragPoint = game.input.activePointer.position.clone();
    } else {
        game.origDragPoint = null;
    }
}

//--//

function initSideBar(sprite){
    // $("#villageOverview").show()
    $("#villageOverview").removeClass("d-none")
    $("#villageOverview").addClass("animated")
    $("#villageOverview").find(".card-title").html("<a href='/game/villages/"+sprite.village_id+"'>"+ sprite.villageName +"</a>")
    $("#villageOverview").find(".card-text")
        .html("Belongs to <a href='/game/players/"+sprite.player_id+"'>"+ sprite.playerName +"</a>")
            .append("<br>"+
                "Village Points = " + sprite.villagePoints)
}

function initSwitchVillage(){
    $(".switchVillage").on('click', function(){
        removePathSprites()
        let switchedVillageCoords = JSON.parse($(this).attr('coords').replace(/'/g, '"'))
        console.log(switchedVillageCoords)
        selectedVillage.coords.x = switchedVillageCoords.x
        selectedVillage.coords.y = switchedVillageCoords.y
    })
}

function removePathSprites(){
    if(pathSprites != undefined){
        pathSprites.forEach(sprite => { 
            sprite.kill()
            console.log(sprite, "killing")
        });
    }
}

function findPath(sourceVillageCoords, targetVillageCoords){
    sourceVillageCoords = JSON.stringify(sourceVillageCoords)
    targetVillageCoords = JSON.stringify(targetVillageCoords)

    let csrftoken = getCookie('csrftoken');
    $.ajax({
        type: 'POST',
        url: '/game/map/findPath',
        data: {
            sourceVillageCoords: sourceVillageCoords,
            targetVillageCoords: targetVillageCoords,
            csrfmiddlewaretoken: csrftoken 
        },
        success:function(data){
            console.log(data, "wololo")
            drawPath(data.path)
        }
    })
}

function drawPath(path){
    var path_positions;
    path_positions = [];
    pathSprites = [];
    console.log(path, typeof(path), "asdadsads")
    if (path !== null) {
        path.forEach(function(path_coord){
            console.log(path_coord)
            let path_position = {
                'x' : path_coord[0],
                'y' : path_coord[1]
            }
            path_positions.push(path_position);
            const pathSprite = game.add.sprite(path_position.x+12, path_position.y+12, 'pathDot');
            pathSprite.alpha = 0.65
            pathSprites.push(pathSprite)
        
        })
        console.log(path, "path")
        console.log(path_positions, "path positions")
        const pathLength = pathSprites.length
        console.log(pathLength, "path length")
    }else{
        console.log("you cant travel through sea, you are not jesus!")
    }
}
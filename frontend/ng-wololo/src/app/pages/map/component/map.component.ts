import { Component, OnInit } from "@angular/core";
import Phaser from "phaser";
import {WoVillageSprite} from "../../../wo-phaser/wo-phaser-sprite/wll-phaser-sprite"

class MapScene extends Phaser.Scene {
  map: Phaser.Tilemaps.Tilemap;
  controls: Phaser.Cameras.Controls.FixedKeyControl;

  constructor() {
    super({ key: "main" });
  }

  create() {
    console.log("create method");
    this.createMap();
    this.cameras.main.setBounds(
      0,
      0,
      this.map.widthInPixels,
      this.map.heightInPixels,
      true
    );
    this.setCursorControls();
    this.loadVillages();
  }

  preload() {
    this.game.scale.scaleMode = Phaser.Scale.FIT;
    this.load.image(
      "tiles",
      "assets/map-assets/tilesets/overworld_tileset_grass.png"
    );
    this.load.tilemapTiledJSON("map", "assets/map-assets/tilemaps/mapv3.json");
    const spriteRoot = "assets/map-assets/sprites/";

    this.load.spritesheet("tr1", spriteRoot + "cultures/turkish/1-48.png", {
      frameWidth: 48,
      frameHeight: 48,
    });
    this.load.spritesheet("tr2", spriteRoot + "cultures/turkish/2-48.png", {
      frameWidth: 48,
      frameHeight: 48,
    });
    this.load.spritesheet("castle", spriteRoot + "castle.png", {
      frameWidth: 48,
      frameHeight: 48,
    });
    this.load.spritesheet("pathDot", spriteRoot + "pathDot.png", {
      frameWidth: 16,
      frameHeight: 16,
    });
    this.load.spritesheet(
      "selected",
      spriteRoot + "selection-circle_1_64x64.png",
      { frameWidth: 64, frameHeight: 64 }
    );
    console.log("preload method");
  }

  update(time, delta) {
    this.drag();
    this.controls.update(delta);
    // console.log("update method");
  }

  private createMap() {
    this.map = this.add.tilemap("map");
    // map will accept inputs

    const tileset = this.map.addTilesetImage("Tile", "tiles");
    let groundLayer = this.map.createStaticLayer("groundLayer", tileset);
    // groundLayer.resizeWorld();
    let seaLayer = this.map.createStaticLayer("seaLayer", tileset);
    // collision layer
    let collision_tiles = [];
    seaLayer.layer.data.forEach(function (data_row) {
      // find tiles used in the layer
      data_row.forEach(function (tile) {
        // check if it's a valid tile index and isn't already in the list
        if (tile.index > 0 && collision_tiles.indexOf(tile.index) === -1) {
          collision_tiles.push(tile.index);
        }
      }, this);
    }, this);
    this.map.setCollision(collision_tiles, true, true, seaLayer.layer.name);
    // seaLayer.resizeWorld();
  }

  origDragPoint;
  private drag() {
    if (this.game.input.activePointer.isDown) {
      if (this.origDragPoint) {
        // move the camera by the amount the mouse has moved since last update
        this.cameras.main.scrollX +=
          this.origDragPoint.x - this.game.input.activePointer.position.x;
        this.cameras.main.scrollY +=
          this.origDragPoint.y - this.game.input.activePointer.position.y;
      } // set new drag origin to current position
      this.origDragPoint = this.game.input.activePointer.position.clone();
    } else {
      this.origDragPoint = null;
    }
  }

  private setCursorControls() {
    //Create cursors to be able to move camera around and their configuration
    let cursors = this.input.keyboard.createCursorKeys();
    this.input.mouse.startListeners();
    let controlConfig = {
      camera: this.cameras.main,
      left: cursors.left,
      right: cursors.right,
      up: cursors.up,
      down: cursors.down,
      speed: 0.5,
      disableCull: true,
      zoomIn: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A),
      zoomOut: this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.E),
    };
    this.controls = new Phaser.Cameras.Controls.FixedKeyControl(controlConfig);
  }

  private loadVillages() {
    let tile_dimensions = new Phaser.Geom.Point(
      this.map.tileWidth,
      this.map.tileHeight
    );

    let infos = [
      {
        playerName: "sdad",
        villagePoints: 150,
        coords: {
          x: 100,
          y: 100
        },
        village_id: "2",
        user_id: 2,
        owner: "yours",
        villageName: "wololo",
        points: 200
      }
    ]

    let parentThis = this;
    infos.forEach(function (element) {
      if (element.playerName != "") {
        let villageImage;
        if (element.villagePoints > 200) {
          villageImage = "tr2";
        } else {
          villageImage = "tr1";
        }

        let mySprite = new WoVillageSprite(parentThis, element.coords.x, element.coords.y, villageImage)
        mySprite.villageId = element.village_id;
        mySprite.userId = element.user_id;
        mySprite.owner = element.owner ? "yours" : "";
        mySprite.villageName = element.villageName;
        mySprite.playerName = element.playerName;
        mySprite.villagePoints = element.points;
        mySprite.x = element.coords.x;
        mySprite.y = element.coords.y;
        parentThis.add.existing(
          mySprite
        );
        
        // sprite.inputEnabled = true;
        // sprite.on("pointerover", function (pointer) {
        //   parentThis.onHoverListener();
        // });
        // sprite.eventNames.add(onHoverListener, sprite);
        // sprite.events.onInputOut.add(onOutListener, sprite);
      }
    });
  }

  // selectedIndicator: Phaser.GameObjects.Sprite;
  // selectedVillage;
  // isVillageSelected: boolean;
  // onClickListener(sprite) {
  //   console.log(this.selectedVillage);
  //   let targetVilCoords = {
  //     x: sprite.x,
  //     y: sprite.y,
  //   };

  //   if (this.isVillageSelected) {
  //     console.log(this.selectedIndicator);
  //     this.selectedIndicator.destroy();
  //     this.isVillageSelected = false;
  //     this.selectedIndicator = this.add.sprite(
  //       sprite.x - 10,
  //       sprite.y - 8,
  //       "selected"
  //     );
  //     this.isVillageSelected = true;
  //     initSideBar(sprite);
  //     removePathSprites();
  //     if (!sprite.owner) {
  //       findPath(this.selectedVillage.coords, targetVilCoords);
  //     }
  //   } else {
  //     this.selectedIndicator = this.add.sprite(
  //       sprite.x - 10,
  //       sprite.y - 8,
  //       "selected"
  //     );
  //     this.isVillageSelected = true;
  //     initSideBar(sprite);

  //     if (!sprite.owner) {
  //       findPath(this.selectedVillage.coords, targetVilCoords);
  //     }
  //   }
  // }

  // onHoverListener(sprite, event) {
  //   document.body.style.cursor = "pointer";

  //   let mousePositionX = event.pageX;
  //   let mousePositionY = event.pageY;
  //   $("#tooltip span").html(
  //     sprite.playerName + "<br>" + sprite.villageName + "<br>" + sprite.owner
  //   );
  //   $("#tooltip").stop(false, true).fadeIn(1000);
  //   $("#tooltip").css({
  //     top: mousePositionY - winH / 18,
  //     left: mousePositionX - winW / 40 + 40,
  //   });

  //   var tooltip = document.querySelectorAll("#tooltip");

  //   function fn(e) {
  //     for (var i = tooltip.length; i--; ) {
  //       tooltip[i].style.left = e.pageX + "px";
  //       tooltip[i].style.top = e.pageY + "px";
  //     }
  //   }

  //   document.addEventListener("mousemove", fn, false);
  // }

  // onOutListener(sprite) {
  //   $("#tooltip").stop(false, true).fadeOut(0);

  //   document.body.style.cursor = "default";
  // }
}

@Component({
  selector: "wo-map",
  templateUrl: "./map.component.html",
  styleUrls: ["./map.component.css"],
})
export class MapComponent implements OnInit {
  game: Phaser.Game;
  config: Phaser.Types.Core.GameConfig;
  constructor() {}
  ngOnInit() {
    const winW: number = document.body.offsetWidth;
    const winH: number = document.body.offsetHeight;
    const height: number = 800;
    const width: number = winW / 2;
    this.config = {
      type: Phaser.AUTO,
      height: height,
      width: width,
      scene: [MapScene],
      parent: "gameContainer",
    };
    this.game = new Phaser.Game(this.config);
  }
}

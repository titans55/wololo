import { Injectable } from "@angular/core";
import { WoVillageSprite } from "src/app/wo-common/wo-phaser-sprite/wo-phaser-sprite";
import { Subject } from "rxjs";
import { VillageDetailCardService } from "../component/village-detail-card/service/village-detail-card.service";
import { Game } from "phaser";
import { MapVillagesService } from "./map-villages.service";

class MapScene extends Phaser.Scene {
  map: Phaser.Tilemaps.Tilemap;
  controls: Phaser.Cameras.Controls.FixedKeyControl;

  constructor(
    public villageDetailCardService: VillageDetailCardService,
    public mapVillagesService: MapVillagesService
  ) {
    super({ key: "main" });
  }

  async create() {
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
    await this.loadVillages();
  }

  preload() {
    // this.load.image(
    //   "tiles",
    //   "assets/ulku-example/tileset.png"
    // );
    // this.load.tilemapTiledJSON("map", "assets/ulku-example/tilemap.json");
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

  selectedIndicator: Phaser.GameObjects.Sprite;
  selectedVillageSubject: Subject<WoVillageSprite> = new Subject();
  selectedVillage: WoVillageSprite;
  private async loadVillages() {
    // let tile_dimensions = new Phaser.Geom.Point(
    //   this.map.tileWidth,
    //   this.map.tileHeight
    // );
    let parentThis = this;

    await this.mapVillagesService.getMapVillages().then((mapVillages) => {
      mapVillages.forEach(function (element) {
        if (element.playerName != "") {
          let villageImageName: string;
          if (element.points > 200) {
            villageImageName = "tr2";
          } else {
            villageImageName = "tr1";
          }

          let mySprite = new WoVillageSprite(
            parentThis,
            element.coords.x,
            element.coords.y,
            villageImageName
          );
          mySprite.villageId = element.villageId.toString();
          mySprite.userId = element.userId;
          mySprite.owner = element.owner ? "yours" : "";
          mySprite.villageName = element.villageName;
          mySprite.playerName = element.playerName;
          mySprite.villagePoints = element.points;
          mySprite.x = element.coords.x;
          mySprite.y = element.coords.y;
          let sprite = <WoVillageSprite>parentThis.add.existing(mySprite);
          sprite.on("pointerdown", () => {
            let targetVilCoords = {
              x: sprite.x,
              y: sprite.y,
            };

            if (parentThis.selectedVillage) {
              console.log(parentThis.selectedIndicator);
              parentThis.selectedIndicator.destroy();
              parentThis.selectedVillage = null;

              // initSideBar(sprite);
              // removePathSprites();
              // if (!sprite.owner) {
              //   findPath(this.selectedVillage.coords, targetVilCoords);
              // }
            } else {
              parentThis.selectedVillageSubject.next(sprite);
              parentThis.villageDetailCardService.villageSelected(sprite);
              parentThis.selectedIndicator = parentThis.add.sprite(
                sprite.x,
                sprite.y,
                "selected"
              );
              parentThis.selectedVillage = sprite;
              // initSideBar(sprite);

              // if (!sprite.owner) {
              //   findPath(this.selectedVillage.coords, targetVilCoords);
              // }
            }
          });
          sprite.on("pointerover", () => {
            // document.body.style.cursor = "pointer";
            // let mousePositionX = event.pageX;
            // let mousePositionY = event.pageY;
            // $("#tooltip span").html(
            //   sprite.playerName + "<br>" + sprite.villageName + "<br>" + sprite.owner
            // );
            // $("#tooltip").stop(false, true).fadeIn(1000);
            // $("#tooltip").css({
            //   top: mousePositionY - winH / 18,
            //   left: mousePositionX - winW / 40 + 40,
            // });
            // var tooltip = document.querySelectorAll("#tooltip");
            // function fn(e) {
            //   for (var i = tooltip.length; i--; ) {
            //     tooltip[i].style.left = e.pageX + "px";
            //     tooltip[i].style.top = e.pageY + "px";
            //   }
            // }
            // document.addEventListener("mousemove", fn, false);
          });
          sprite.setInteractive();

          // sprite.inputEnabled = true;
          // sprite.on("pointerover", function (pointer) {
          //   parentThis.onHoverListener();
          // });
          // sprite.eventNames.add(onHoverListener, sprite);
          // sprite.events.onInputOut.add(onOutListener, sprite);
        }
      });
    });
  }

  // onHoverListener(sprite, event) {

  // }

  // onOutListener(sprite) {
  //   $("#tooltip").stop(false, true).fadeOut(0);

  //   document.body.style.cursor = "default";
  // }
}

@Injectable({
  providedIn: "root",
})
export class MapSceneService {
  mapScene: Phaser.Scene;

  constructor(
    public villageDetailCardService: VillageDetailCardService,
    public mapVillagesService: MapVillagesService
  ) {}

  getNewInstanceOfMapScene() {
    return new MapScene(this.villageDetailCardService, this.mapVillagesService);
  }
}

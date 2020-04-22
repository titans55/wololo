import { Component, OnInit } from "@angular/core";
import Phaser from "phaser";
import { MapSceneService } from "../service/map-scene.service";
@Component({
  selector: "wo-map",
  templateUrl: "./map.component.html",
  styleUrls: ["./map.component.css"],
})
export class MapComponent implements OnInit {
  game: Phaser.Game;
  config: Phaser.Types.Core.GameConfig;
  constructor(public mapSceneService: MapSceneService) {}
  ngOnInit() {
    const winW: number = document.body.offsetWidth;
    const winH: number = document.body.offsetHeight;
    const height: number = 800;
    const width: number = winW / 2;
    this.config = {
      type: Phaser.AUTO,
      height: height,
      width: width,
      scene: [this.mapSceneService],
      parent: "gameContainer",
    };
    this.game = new Phaser.Game(this.config);
  }
}

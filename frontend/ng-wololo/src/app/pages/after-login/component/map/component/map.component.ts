import { Component, OnInit } from "@angular/core";
import Phaser, { Game } from "phaser";
import { MapSceneService } from "../service/map-scene.service";
import { WoVillageSprite } from "src/app/wo-common/wo-phaser-sprite/wo-phaser-sprite";
import { VillageDetailCardService } from "./village-detail-card/service/village-detail-card.service";
@Component({
  selector: "wo-map",
  templateUrl: "./map.component.html",
  styleUrls: ["./map.component.css"],
})
export class MapComponent {
  /**
   * Game instance.
   */
  public game: Phaser.Game;
  // public scene: Phaser.Scene;

  /**
   * Phaser API.
   */
  public readonly phaser = Phaser;

  public readonly gameConfig: Phaser.Types.Core.GameConfig = {
    title: "Wololo the best strategy game",
    type: Phaser.AUTO,
    width: 700,
    height: 550,
  };

  constructor(public mapSceneService: MapSceneService) {}

  public onGameReady(game: Phaser.Game): void {
    this.game = game;
    this.game.scene.add(
      "main",
      this.mapSceneService.getNewInstanceOfMapScene(),
      true
    );
  }
}

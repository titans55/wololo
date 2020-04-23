export class WoVillageSprite extends Phaser.GameObjects.Sprite {
    villageId: string;
    villageName: string;
    userId: number;
    owner: string;
    playerName: string;
    villagePoints: number;
    customAttributes: any;
    constructor(scene: Phaser.Scene, x: number, y: number, key: string ){
        super(scene, x, y, key)
    }
}

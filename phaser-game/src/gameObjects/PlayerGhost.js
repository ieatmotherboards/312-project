export class PlayerGhost {

    constructor(scene, x, y) {
        this.scene = scene;
        this.sprite = this.scene.add.sprite(x, y, 'ghost').setScale(.5, .5);
    }
}
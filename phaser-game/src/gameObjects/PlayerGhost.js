export class PlayerGhost {

    constructor(scene, x, y, username) {
        this.scene = scene;
        this.sprite = this.scene.add.sprite(x, y, 'ghost').setScale(.5, .5);
        this.username = username;
    }

    move(x, y) {
        this.sprite.setX(x).setY(y);
    }
}
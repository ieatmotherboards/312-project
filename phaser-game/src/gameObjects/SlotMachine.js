export class SlotMachine {

    constructor(scene, x, y, key) {
        this.scene = scene;
        this.sprite = this.scene.physics.add.staticSprite(x, y, key).setScale(2.5, 2.5).refreshBody();

        this.scene.physics.add.collider(this.sprite, this.scene.player);

        this.DEBUG = true;
    }

    addOverlapBox(xOff, yOff, scale) {
        this.overlap = this.scene.physics.add.staticSprite(this.sprite.x + xOff, this.sprite.y + yOff).setScale(scale);
        if (this.DEBUG) {
            this.overlap.setTexture('debug');
            this.overlap.setAlpha(0.5);
        }
        this.scene.physics.add.overlap(this.overlap, this.scene.player, this.playerCollide, null, this);
        this.overlap.refreshBody();
    }

    playerCollide() {
        console.log('interacted');
    }
}
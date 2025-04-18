export class SlotMachine extends Phaser.Physics.Arcade.Sprite {

    constructor(scene, x, y, key) {
        super(scene, x, y, key);
        this.scene.add.existing(this);
        // this.scene.physics.add.existing(this);

        this.scene.physics.add.collider(this, this.scene.player);

        this.DEBUG = true
    }

    addOverlapBox(xOff, yOff, scale) {
        this.overlap = this.scene.physics.add.staticSprite(this.x + xOff, this.y + yOff).setScale(scale);
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
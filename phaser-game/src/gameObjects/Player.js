export class Player extends Phaser.Physics.Arcade.Sprite
{
    constructor(scene, x, y) {
        super(scene, x, y, 'pfp')
        this.setDisplaySize(34, 34);
        this.scene.add.existing(this);
        this.scene.physics.add.existing(this);

        this.border = this.scene.add.sprite(x, y, 'ghost').setDisplaySize(36, 36);

        this.setCollideWorldBounds(true);   // enables player collision with world bounds
    }

    // these methods handle movement and are called by the parent scene
    move(x, y) {
        this.setVelocityX(x);
        // if (x > 0) {
        //     this.anims.play('right', true);
        // } else if (x < 0) {
        //     this.anims.play('left', true);
        // }
        this.setVelocityY(y);
        // if (x == 0 && y == 0) {
        //     this.anims.play('turn');
        // }
        this.border.setX(this.x).setY(this.y);
    }
}
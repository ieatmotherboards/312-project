export class Player extends Phaser.Physics.Arcade.Sprite
{
    constructor(scene, x, y) {
        super(scene, x, y, 'dude');
        this.scene.add.existing(this);
        this.scene.physics.add.existing(this);

        this.setCollideWorldBounds(true);   // enables player collision with world bounds
        this.initAninations();
    }

    // initializes player's animations (from tutorial) (maybe won't use later)
    initAninations() {
        this.anims.create({
            key: 'left',
            frames: this.anims.generateFrameNumbers('dude', {start: 0, end: 3}),
            frameRate: 10,
            repeat: -1
        });
        
        this.anims.create({
            key: 'turn',
            frames: [{key: 'dude', frame: 4}],
            frameRate: 1
        });

        this.anims.create({
            key: 'right',
            frames: this.anims.generateFrameNumbers('dude', {start: 5, end: 8}),
            frameRate: 10,
            repeat: -1
        });
    }

    // these methods handle movement and are called by the parent scene
    move(x, y) {
        this.setVelocityX(x);
        if (x > 0) {
            this.anims.play('right', true);
        } else if (x < 0) {
            this.anims.play('left', true);
        }
        this.setVelocityY(y);
        if (x == 0 && y == 0) {
            this.anims.play('turn');
        }
    }
}
export class Player extends Phaser.Physics.Arcade.Sprite
{
    constructor(scene, x, y) {
        super(scene, x, y, 'dude');
        scene.add.existing(this);
        scene.physics.add.existing(this);

        this.setCollideWorldBounds(true);   // enables player collision with world bounds
        this.initAninations();      

        this.score = 0; // score variable from tutorial
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
    moveLeft() {
        this.setVelocityX(-200);
        this.anims.play('left', true)
    }

    moveRight() {
        this.setVelocityX(200);
        this.anims.play('right', true)
    }

    moveUp() {
        this.setVelocityY(-200);
    }

    moveDown() {
        this.setVelocityY(200);
    }

    idleX() {
        this.setVelocityX(0);
    }
    
    idleY() {
        this.setVelocityY(0);
    }

    idle() {
        this.anims.play('turn');
    }
}
import { Player } from '../gameObjects/Player.js';

export class Game extends Phaser.Scene {
    constructor() {
        super('Game');

    }

    create() {
        this.add.image(400, 300, 'sky');

        this.platforms = this.physics.add.staticGroup();

        this.platforms.create(400, 568, 'platform').setScale(2).refreshBody();

        this.platforms.create(600, 400, 'platform');
        this.platforms.create(50, 250, 'platform');
        this.platforms.create(720, 220, 'platform');

        this.player = new Player(this, 100, 450);
        this.physics.add.collider(this.player, this.platforms);
        
        this.cursors = this.input.keyboard.createCursorKeys();

        this.stars = this.physics.add.group({
            key: 'star',
            repeat: 11,
            setXY: {x: 12, y: 0, stepX: 70},
            gravityY: 500
        });

        this.stars.children.iterate( child =>{
            child.setBounceY(Phaser.Math.FloatBetween(.4, .8));
        });

        this.physics.add.collider(this.stars, this.platforms);
        this.physics.add.overlap(this.player, this.stars, this.collectStar, null, this);

        this.scoreText = this.add.text(16, 16, 'Stars Collected: 0', { fontSize: '32px', fill: '#000' });
    }

    update(time) {
        let moved = false
        if (this.cursors.left.isDown) {
            this.player.moveLeft();
            moved = true;
        }
        else if (this.cursors.right.isDown) {
            this.player.moveRight();
            moved = true;
        }
        else {
            this.player.idleX();
        }
        if (this.cursors.up.isDown) {
            this.player.moveUp();
            moved = true;
        }
        else if (this.cursors.down.isDown) {
            this.player.moveDown();
            moved = true;
        }
        else {
            this.player.idleY();
        }
        if (!moved) {
            this.player.idle();
        }
    }

    collectStar(player, star) {
        star.disableBody(true, true);
        
        this.player.score += 1;
        this.scoreText.setText('Stars Collected: ' + this.player.score);
    }

}
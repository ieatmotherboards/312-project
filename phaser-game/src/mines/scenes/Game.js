export class Game extends Phaser.Scene {
    constructor() {
        super('Game');

    }

    create() {
        this.add.image(400, 300, 'cave');

        this.coal = this.add.sprite(400, 300, 'coal').setInteractive().setScale(4, 4);
        this.breaking = false

        this.coal.on('pointerdown', function (pointer) {
            if (!this.breaking) {
                this.setTexture('coal_breaking');
                this.breaking = true;
            } else {
                this.visible = false;
                this.coin = this.scene.physics.add.sprite(this.x, this.y, 'coin');
                this.coin.setScale(2.5, 2.5);
                this.coin.setGravityY(500);
                this.coin.setBounceY(0.5);
                this.coin.setCollideWorldBounds(true);
            }
        });
        
        this.cursors = this.input.keyboard.createCursorKeys();

   }

}
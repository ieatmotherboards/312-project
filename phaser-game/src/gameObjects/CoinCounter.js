export class CoinCounter extends Phaser.GameObjects.Sprite {

    constructor(scene, x, y) {
        super(scene, x, y, 'coin');
        this.setDisplaySize(32, 32);
        scene.add.existing(this);
        this.coins = 0;

        this.text = scene.add.text(x + 20, y - 12, "x0", { fontSize: '32px', fill: '#000' });
    }

    setCoins(c) {
        this.coins = c;
        this.text.setText("x" + this.coins);
    }

    incrementCoins() {
        this.setCoins(this.coins + 1);
    }
}

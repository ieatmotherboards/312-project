export class CoinCounter extends Phaser.GameObjects.GameObject {

    constructor(scene, x, y) {
        super(scene, x, y, 'coin');
        this.coinSprite = this.scene.add.image(x, y, 'coin').setDisplaySize(32, 32).setDepth(2);
        this.coins = 0;
        this.bg = this.scene.add.image(x - 18, y, 'cc_bg').setDisplaySize(150, 38).setDepth(1).setOrigin(0, 0.5);

        this.x_text = this.scene.add.text(x + 15, y + 4, "x", { fontSize: '32px', fill: '#FFF' }).setOrigin(0, 0.5).setDepth(2);
        this.coin_text = this.scene.add.text(x + 35, y + 5, "0", { fontSize: '32px', fill: '#FFF' }).setOrigin(0, 0.5).setDepth(2);
    }

    updateDisplay() {
        this.coin_text.setText(this.coins);
        // setting base fontsize of 32
        this.coin_text.setStyle({ fontSize: 32});
        console.log(this.coin_text.width);
        let size = 32;
        // let size = this.coin_text.style.fontSize;
        // size = Number(size.substring(0, size.length - 2));

        // if text width is > 97px, shrink font size
        while (this.coin_text.width > 97 && size > 4) {
            size--;
            this.coin_text.setStyle({ fontSize: size});
        }
    }

    setCoins(c) {
        this.coins = c;
        this.updateDisplay();
    }

    incrementCoins() {
        this.setCoins(this.coins + 1);
    }

    addCoins(c) {
        this.setCoins(this.coins + c);
    }
}

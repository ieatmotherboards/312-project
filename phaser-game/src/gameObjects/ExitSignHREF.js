export class ExitSignHREF extends Phaser.GameObjects.Sprite {

    constructor(scene, x, y, hrefKey) {
        super(scene, x, y, 'exit');
        this.setScale(2);
        scene.add.existing(this);
        this.setInteractive();
        this.on('pointerdown', pointer => {
            this.scene.changePage();
            window.location.href = hrefKey;
        });
    }
}
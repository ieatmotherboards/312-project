export class ExitSign2 extends Phaser.GameObjects.Sprite {

    constructor(scene, x, y, sceneKey) {
        super(scene, x, y, 'exit');
        this.setScale(2);
        scene.add.existing(this);
        this.setInteractive();
        this.on('pointerdown', pointer => {
            window.location.href = '/';
        });
    }
}
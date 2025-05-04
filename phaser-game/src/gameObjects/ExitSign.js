export class ExitSign extends Phaser.GameObjects.Sprite {

    constructor(scene, x, y, sceneKey) {
        super(scene, x, y, 'exit');
        this.setScale(2);
        scene.add.existing(this);
        this.setInteractive();
        this.on('pointerdown', pointer => {
            this.scene.scene.start(sceneKey);
            this.scene.changeScene();
        });
    }
}
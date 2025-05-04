export class Boot extends Phaser.Scene
{
    constructor ()
    {
        super('Boot');
    }

    preload ()
    {
        //  The Boot Scene is typically used to load in any assets you require for your Preloader, such as a game logo or background.
        //  The smaller the file size of the assets, the better, as the Boot Scene itself has no preloader.

        this.load.setPath('phaser-game/assets');
        this.load.image('background', 'bg.png');
        this.load.image('debug', 'debug.png');
    }

    create ()
    {
        this.scene.start('Preloader');
    }
}

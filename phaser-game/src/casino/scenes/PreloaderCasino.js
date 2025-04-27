export class Preloader extends Phaser.Scene {
    constructor() {
        super('Preloader');
    }

    init() {
        //  We loaded this image in our Boot Scene, so we can display it here
        this.add.image(512, 384, 'background');

        //  A simple progress bar. This is the outline of the bar.
        this.add.rectangle(512, 384, 468, 32).setStrokeStyle(1, 0xffffff);

        //  This is the progress bar itself. It will increase in size from the left based on the % of progress.
        const bar = this.add.rectangle(512 - 230, 384, 4, 28, 0xffffff);

        //  Use the 'progress' event emitted by the LoaderPlugin to update the loading bar
        this.load.on('progress', (progress) => {

            //  Update the progress bar (our bar is 464px wide, so 100% = 464px)
            bar.width = 4 + (460 * progress);

        });
    }

    preload() {
        this.load.setPath('phaser-game/assets');
        this.load.image('sky', 'sky.png');
        this.load.image('phaser', 'phaser.png');

        // casino floor imgs
        this.load.image('slotmachine', 'slotmachine.png');
        this.load.image('slotmachine_side', 'slotmachine_side.png');
        this.load.image('coin', 'coin.png');
        this.load.image('popup', 'play_popup.png');
        this.load.image('ghost', 'pfp_border.png');
        this.load.image('exit', 'exit_sign.png');
        this.load.spritesheet('dude', 'dude.png', {frameWidth: 32, frameHeight: 48});

        // slot machine imgs
        this.load.setPath('phaser-game/assets/slots');
        this.load.image('slots_bg', 'slots_bg.png');
        this.load.image('button', 'spin_button.png');
        this.load.spritesheet('slot_icons', 'slots_icons.png', {frameWidth: 32, frameHeight: 32});

        // coin flip imgs
        this.load.setPath('phaser-game/assets/coin_toss');
        this.load.spritesheet('coin_flip', 'coin_flip.png', {frameWidth: 128, frameHeight: 128});
    }

    create() {
        this.scene.start('Game');
    }
}

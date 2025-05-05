export class Preloader extends Phaser.Scene {
    constructor() {
        super('Preloader');
    }

    init() {
        const width = this.scale.width;
        const height = this.scale.height;
        //  We loaded this image in our Boot Scene, so we can display it here
        this.add.image(width * 0.5, height * 0.5, 'background').setDisplaySize(width, height);

        //  A simple progress bar. This is the outline of the bar.
        this.add.rectangle(width * 0.5, height * 0.5, 468, 32).setStrokeStyle(1, 0xffffff);

        //  This is the progress bar itself. It will increase in size from the left based on the % of progress.
        const bar = this.add.rectangle(width * 0.5 - 230, height * 0.5, 4, 28, 0xffffff);

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
        this.load.image('back', 'back_mod.png');
        this.load.image('youwin', 'youwin.png');
        this.load.image('youlose', 'youlose.png');
        this.load.image('up1', 'up1.png');
        this.load.image('up5', 'up5.png');
        this.load.image('down1', 'down1.png');
        this.load.image('down5', 'down5.png');
        this.load.image('cc_bg', 'coin_counter_bg.png');

        // casino floor imgs
        this.load.image('slotmachine', 'slotmachine.png');
        this.load.image('slotmachine_side', 'slotmachine_side.png');
        this.load.image('coin', 'coin.png');
        this.load.image('popup', 'play_popup.png');
        this.load.image('ghost', 'pfp_border.png');
        this.load.image('exit', 'exit_sign.png');
        this.load.image('challenge_screen', 'challenge_screen.png');
        this.load.image('mine_entrance', 'mine_entrance.png');
        this.load.image('pfp', 'placeholder_pfp.png');
        this.load.image('roulette_table', 'roulette_table.png');
        // this.load.spritesheet('dude', 'dude.png', {frameWidth: 32, frameHeight: 48});

        // mines imgs
        this.load.setPath('phaser-game/assets/mines');
        this.load.image('cave', 'cave.png');
        this.load.image('coal', 'coal.png');
        this.load.image('coal_breaking', 'coal_breaking.png');

        // slot machine imgs
        this.load.setPath('phaser-game/assets/slots');
        this.load.image('slots_bg', 'slots_bg.png');
        this.load.image('button', 'spin_button.png');
        this.load.image('line_h', 'slots_line_h.png');
        this.load.image('line_d', 'slots_line_d.png');
        this.load.spritesheet('slot_icons', 'slots_icons.png', {frameWidth: 32, frameHeight: 32});

        // coin flip imgs
        this.load.setPath('phaser-game/assets/coin_toss');
        this.load.image('table', 'crust_table.png');
        this.load.spritesheet('coin_flip', 'coin_flip.png', {frameWidth: 128, frameHeight: 128});
    }

    create() {
        this.scene.start('Game');
    }
}

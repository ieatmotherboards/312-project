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
        this.load.image('back', 'back_mod.png');
        this.load.image('youwin', 'youwin.png');
        this.load.image('youlose', 'youlose.png');
        this.load.image('up1', 'up1.png');
        this.load.image('up5', 'up5.png'); 
        this.load.image('down1', 'down1.png'); 
        this.load.image('down5', 'down5.png'); 

        // casino floor imgs
        this.load.image('coin', 'coin.png');
        this.load.image('popup', 'play_popup.png');
        this.load.image('ghost', 'pfp_border.png');
        this.load.image('exit', 'exit_sign.png');
        this.load.image('challenge_screen', 'challenge_screen.png');
        this.load.image('mine_entrance', 'mine_entrance.png');
        this.load.image('pfp', 'placeholder_pfp.png');
        // this.load.spritesheet('dude', 'dude.png', {frameWidth: 32, frameHeight: 48});

        // roulette imgs
        this.load.setPath('phaser-game/assets/roulette');
        this.load.image('roulette_bg', 'roulette_bg_2.png'); 
        this.load.image('wheel', 'roulette_wheel.png'); 
        this.load.image('ball', 'ball.png');
        this.load.image('place_bet', 'place_bet.png');
    }

    create() {
        this.scene.start('Roulette');
    }
}

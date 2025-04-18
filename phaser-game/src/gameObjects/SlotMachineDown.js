import { SlotMachine } from './SlotMachine.js'

export class SlotMachineDown extends SlotMachine {

    constructor(scene, x, y) {
        super(scene, x, y, 'slotmachine');
        this.addOverlapBox(0, 30, 2);
    }
}
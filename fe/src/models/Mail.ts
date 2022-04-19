export interface MailInterface {
    url: string
    id: number
    sender: string
    receiver: string
    time: string
    info: string
}

export class Mail implements MailInterface {
    id: number;
    info: string;
    receiver: string;
    sender: string;
    time: string;
    url: string;

    constructor(obj: MailInterface);
    constructor(
        id: number,
        info: string,
        receiver: string,
        sender: string,
        time: string,
        url: string
    );

    constructor(...args: any[]) {
        if (args.length == 1) {
            Object.assign(this, args[0])
        } else {
            this.id = args[0]
            this.info = args[1]
            this.receiver = args[2]
            this.sender = args[3]
            this.time = args[4]
            this.url = args[5]
        }
    }
}
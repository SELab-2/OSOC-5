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

    constructor(
        id: number,
        info: string,
        receiver: string,
        sender: string,
        time: string,
        url: string
    ) {
        this.id = id
        this.info = info
        this.receiver = receiver
        this.sender = sender
        this.time = time
        this.url = url
    }
}
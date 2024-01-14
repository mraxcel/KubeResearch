# PYTHON_ARGCOMPLETE_OK
import argcomplete
import argparse

from kubr.backends.volcano import VolcanoBackend
from kubr.commands.desc import DescribeCommand
from kubr.commands.logs import LogsCommand
from kubr.commands.ls import LsCommand
from kubr.commands.rm import RmCommand
from kubr.commands.run import RunCommand


def main():
    # TODO fix package install adding eval in bash\zsh for autocomplete
    # adding eval "$(register-python-argcomplete kubr)" to .bashrc or .zshrc

    backend = VolcanoBackend()
    arg = argparse.ArgumentParser(description='Kubr', add_help=True)
    arg.add_argument('--version', help='Get version of Kubr')
    subparsers = arg.add_subparsers(help='Commands', dest='command')

    run_parser = RunCommand.add_parser(subparsers)
    ls_parser = LsCommand.add_parser(subparsers)
    rm_parser = RmCommand.add_parser(subparsers, completer=backend._completion_list_running_jobs)
    desc_parser = DescribeCommand.add_parser(subparsers, completer=backend._completion_list_running_jobs)
    logs_parser = LogsCommand.add_parser(subparsers, completer=backend._completion_list_running_jobs)

    # attach_parser = subparsers.add_parser('attach', help='Attach to a job')
    # attach_parser.add_argument('job', help='Name of job to attach to')
    #
    # stat_parser = subparsers.add_parser('stat', help='Get stats of a cluster')

    argcomplete.autocomplete(arg)
    args = arg.parse_args()

    if args.command == 'run':
        operator = RunCommand()
        print(operator(config=args.config, image=args.image, entrypoint=args.entrypoint, namespace=args.namespace,
                       name=args.name))
    elif args.command == 'ls':
        operator = LsCommand()
        print(operator(namespace=args.namespace, show_all=args.all, head=args.top))
    elif args.command == 'rm':
        operator = RmCommand()
        print(operator(job_name=args.job, namespace=args.namespace))
    elif args.command == 'desc':
        operator = DescribeCommand()
        print(operator(job_name=args.job_name, namespace=args.namespace))
    elif args.command == 'logs':
        operator = LogsCommand()
        print(operator(job_name=args.job, namespace=args.namespace, tail=args.tail))
    elif args.command == 'attach':
        raise NotImplementedError  # TODO implement attach command
    elif args.command == 'stat':
        raise NotImplementedError  # TODO implement stat command
    elif args.command == 'test':
        raise NotImplementedError  # TODO implement test command -- run IB\scheduler\metrics\registry\ethernet tests
    else:
        arg.print_help()


if __name__ == '__main__':
    main()

